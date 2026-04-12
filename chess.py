import ttkbootstrap as ttk
from typing import Optional, Union
import tkinter.font as tkfont

DEFAULT_FONTSIZE  = 14
DEFAULT_FONTNAME  = 'Arial'
DEFAULT_FONTCOLOR = (0, 0, 0)

game_objects        = []
interactive_objects = []

# ─────────────────────────────────────────────
#  ENGINE CLASSES
# ─────────────────────────────────────────────

class Rect:
    def __init__(self, x: float, y: float, w: float, h: float,
                 color, *,
                 draw_from=None, text=None, label=None, label_type='position',
                 font_size=DEFAULT_FONTSIZE, font_name=DEFAULT_FONTNAME,
                 font_color=DEFAULT_FONTCOLOR, show_center=False, bold=False,
                 text_padding=0, autofit_text=False, autofit_rect=True,
                 ground_y=None, gravity=0.0, collidable=False, normal_force=True,
                 is_ui=False, anchor_panel=None, panel_position=None,
                 border_radius=0, auto_register=True, is_interactive=False):

        draw_from = draw_from or 'topleft'

        if anchor_panel is not None and panel_position is not None:
            pos = anchor_panel.get_position(panel_position)
            if pos: x, y = pos

        self.x = float(x);  self.y = float(y)
        self.w = float(w);  self.h = float(h)
        self.base_w = float(w);  self.base_h = float(h)
        self.color = self._handle_color(color) if isinstance(color, tuple) else color
        self.gravity   = gravity
        self.vy = self.vx = self.ax = self.ay = self.dvx = self.dvy = 0.0
        self.ox = self.x;  self.oy = self.y
        self.autofit_text  = autofit_text;  self.autofit_rect = autofit_rect
        self.draw_from     = draw_from;     self.text         = text
        self.label         = label;          self.label_type   = label_type
        self.font_name     = font_name;      self.font_color   = font_color
        self.visible_center= show_center;    self.bold         = bold
        self.text_padding  = text_padding;   self.ground_y     = ground_y
        self.normal_force  = normal_force;   self.collidable   = collidable
        self.border_radius = border_radius
        self._cached_font  = tkfont.Font(family=font_name, size=font_size,
                                          weight='bold' if bold else 'normal')
        self.font_size = self._process_font_size(font_size) if autofit_text else font_size
        self._process_rect();  self._handle_kwargs()

        if auto_register:
            game_objects.append(self)
            if is_interactive:
                interactive_objects.append(self)

    def _handle_color(self, color):
        return '#%.02x%.02x%.02x' % color

    def _process_font_size(self, font_size):
        if isinstance(self.text_padding, (int, float)):
            aw = self.w - 2*self.text_padding;  ah = self.h - 2*self.text_padding
        elif isinstance(self.text_padding, tuple):
            aw = self.w - self.text_padding[0]*2;  ah = self.h - self.text_padding[1]*2
        else:
            aw = self.w;  ah = self.h
        lo, hi, best = 1, font_size, 1
        txt = self.text if isinstance(self.text, str) else (self.text[0] if isinstance(self.text, tuple) else '')
        while lo <= hi:
            mid = (lo+hi)//2
            f = tkfont.Font(family=self.font_name, size=mid, weight='bold' if self.bold else 'normal')
            if f.measure(txt) <= aw and f.metrics('linespace') <= ah:
                best = mid;  lo = mid+1
            else:
                hi = mid-1
        return best

    def _process_rect(self):
        self.w = self.base_w;  self.h = self.base_h
        txt = self.text if isinstance(self.text, str) else (self.text[0] if isinstance(self.text, tuple) else '')
        tw = self._cached_font.measure(txt);  th = self._cached_font.metrics('linespace')
        if isinstance(self.text_padding, (int, float)):
            aw = self.w - 2*self.text_padding;  ah = self.h - 2*self.text_padding
        elif isinstance(self.text_padding, tuple):
            aw = self.w - self.text_padding[0]*2;  ah = self.h - self.text_padding[1]*2
        else:
            aw = self.w;  ah = self.h
        if tw > aw: self.w += tw - aw
        if th > ah: self.h += th - ah

    def _handle_kwargs(self):
        self.draw_x = self.x;  self.draw_y = self.y
        if self.draw_from == 'center':
            self.draw_x = self.x - self.w/2
            self.draw_y = self.y - self.h/2

    def _get_text_params(self, idx, default=None):
        return self.text[idx] if isinstance(self.text, tuple) and len(self.text) > idx else default

    def _draw_text(self, canvas):
        if isinstance(self.text, str):
            ts, tz, tc, tf = self.text, self.font_size, self.font_color, self.font_name
        elif isinstance(self.text, tuple):
            ts = self._get_text_params(0, '')
            tz = self._get_text_params(1, self.font_size)
            tc = self._get_text_params(2, self.font_color)
            tf = self._get_text_params(3, self.font_name)
        else:
            return
        if isinstance(tc, tuple): tc = '#%.02x%.02x%.02x' % tc
        cx = self.x if self.draw_from == 'center' else self.x + self.w/2
        cy = self.y if self.draw_from == 'center' else self.y + self.h/2
        te = Text(cx, cy, ts, font_size=tz or self.font_size,
                  font_color=tc or self.font_color, font_name=tf or self.font_name)
        te.draw(canvas)
        self.text_id = te.text_id

    def _create_rounded_rectangle(self, canvas, x1, y1, x2, y2, r):
        pts = [(x1+r,y1),(x2-r,y1),(x2,y1),(x2,y1+r),(x2,y2-r),(x2,y2),
               (x2-r,y2),(x1+r,y2),(x1,y2),(x1,y2-r),(x1,y1+r),(x1,y1)]
        if isinstance(self.color, tuple): self.color = self._handle_color(self.color)
        return canvas.create_polygon(pts, fill=self.color, smooth=True, outline='')

    def draw(self, canvas):
        if isinstance(self.color, tuple): self.color = self._handle_color(self.color)
        if self.border_radius > 0:
            self.rect_id = self._create_rounded_rectangle(
                canvas, self.draw_x, self.draw_y,
                self.draw_x+self.w, self.draw_y+self.h, self.border_radius)
        else:
            self.rect_id = canvas.create_rectangle(
                self.draw_x, self.draw_y,
                self.draw_x+self.w, self.draw_y+self.h, fill=self.color, outline='')
        if self.text is not None:
            self._draw_text(canvas)

    def check_click(self, cx, cy, is_use):
        if not is_use: return False
        return self.draw_x <= cx <= self.draw_x+self.w and self.draw_y <= cy <= self.draw_y+self.h

    def update(self, canvas):
        ch = canvas.winfo_height()
        if ch <= 1: return
        self.vy += self.gravity - self.dvy;  self.vx += self.dvx
        self.dvy = self.dvx = 0.
        gy = ch - self.ground_y if isinstance(self.ground_y, float) else ch
        if self.y + self.h + self.vy >= gy:
            if self.normal_force: self.y = gy - self.h;  self.vy = 0
        else:
            self.y += self.vy;  self.x += self.vx
        self.base_w = self.w;  self.base_h = self.h
        self._process_rect();  self._handle_kwargs()
        dx = self.x - self.ox;  dy = self.y - self.oy
        for attr in ('rect_id','text_id','label_id','center_point'):
            if hasattr(self, attr): canvas.move(getattr(self, attr), dx, dy)
        self.ox = self.x;  self.oy = self.y


class Panel(Rect):
    def __init__(self, x, y, w, h, color, *, draw_from='topleft', text=None,
                 font_size=DEFAULT_FONTSIZE, font_name=DEFAULT_FONTNAME,
                 font_color=DEFAULT_FONTCOLOR, show_center=False, bold=False,
                 text_padding=0, border_radius=25, positions=None,
                 anchor_panel=None, panel_position=None,
                 auto_register=True, is_interactive=False):
        super().__init__(x, y, w, h, color, draw_from=draw_from, text=text,
                         font_size=font_size, font_name=font_name, font_color=font_color,
                         show_center=show_center, bold=bold, text_padding=text_padding,
                         anchor_panel=anchor_panel, panel_position=panel_position,
                         border_radius=border_radius, auto_register=auto_register,
                         is_interactive=is_interactive)
        self.positions = positions.copy() if positions else {}

    def add_position(self, n, rx, ry): self.positions[n] = (rx, ry)
    def get_position(self, n):
        if n in self.positions:
            rx, ry = self.positions[n]
            return (self.x+rx, self.y+ry)
        return None


class Button(Rect):
    def __init__(self, x, y, w, h, color, text, on_click=None, *,
                 hover_color=None, pressed_color=None, disabled_color=None,
                 disabled=False, **kwargs):
        super().__init__(x, y, w, h, color, text=text, is_interactive=True, **kwargs)
        self.on_click       = on_click
        self.hover_color    = hover_color    or self._lighten_color(color,  0.2)
        self.pressed_color  = pressed_color  or self._lighten_color(color, -0.2)
        self.disabled_color = disabled_color or self._lighten_color(color, -0.1)
        self.disabled = disabled;  self.is_hovered = False
        self.is_pressed = False;   self.original_color = color

    def _lighten_color(self, color, f):
        if isinstance(color, str): return color
        r, g, b = color
        if f > 0:
            r = min(255, int(r+(255-r)*f));  g = min(255, int(g+(255-g)*f));  b = min(255, int(b+(255-b)*f))
        else:
            r = max(0, int(r*(1+f)));  g = max(0, int(g*(1+f)));  b = max(0, int(b*(1+f)))
        return self._handle_color((r, g, b))

    def update_color(self):
        self.color = (self.disabled_color if self.disabled else
                      self.pressed_color  if self.is_pressed else
                      self.hover_color    if self.is_hovered else
                      self.original_color)

    def check_hover(self, mx, my):
        was = self.is_hovered
        self.is_hovered = (self.draw_x <= mx <= self.draw_x+self.w and
                           self.draw_y <= my <= self.draw_y+self.h and not self.disabled)
        if was != self.is_hovered: self.update_color();  return True
        return False

    def handle_click(self, mx, my):
        if self.is_hovered and not self.disabled and self.on_click:
            self.is_pressed = True;  self.update_color();  self.on_click();  return True
        return False

    def release_click(self):
        if self.is_pressed: self.is_pressed = False;  self.update_color();  return True
        return False

    def update(self, canvas):
        self.update_color();  super().update(canvas)


class Text:
    def __init__(self, x, y, text, *, font_size=DEFAULT_FONTSIZE,
                 font_name=DEFAULT_FONTNAME, bold=False, font_color='black',
                 anchor='center', justify='center'):
        self.x = float(x);  self.y = float(y);  self.text = text
        self.font  = (font_name, font_size, 'bold') if bold else (font_name, font_size)
        self.fillc = font_color;  self.anchor = anchor;  self.justify = justify
        _a = {'center':'center','topleft':'nw','topright':'ne','bottomleft':'sw',
              'bottomright':'se','top':'n','bottom':'s','right':'e','left':'w'}
        self.draw_anchor = _a.get(anchor, 'center')

    def draw(self, canvas):
        if isinstance(self.fillc, tuple):
            self.fillc = '#%.02x%.02x%.02x' % self.fillc
        self.text_id = canvas.create_text(
            self.x, self.y, text=self.text, font=self.font,
            justify=self.justify, anchor=self.draw_anchor, fill=self.fillc)


# ─────────────────────────────────────────────
#  CHESS COLOURS & UNICODE
# ─────────────────────────────────────────────

PIECES_UNICODE = {
    'wK':'♔','wQ':'♕','wR':'♖','wB':'♗','wN':'♘','wP':'♙',
    'bK':'♚','bQ':'♛','bR':'♜','bB':'♝','bN':'♞','bP':'♟',
}
LIGHT_SQ    = (240, 217, 181)
DARK_SQ     = (181, 136,  99)
SEL_COLOR   = ( 20, 120,  40)
HINT_COLOR  = (100, 200, 100)
CHECK_COLOR = (200,  40,  40)
PANEL_COLOR = ( 50,  50,  50)

# ─────────────────────────────────────────────
#  CHESS LOGIC (pure functions)
# ─────────────────────────────────────────────

def init_board():
    return [
        ['bR','bN','bB','bQ','bK','bB','bN','bR'],
        ['bP','bP','bP','bP','bP','bP','bP','bP'],
        [None]*8,[None]*8,[None]*8,[None]*8,
        ['wP','wP','wP','wP','wP','wP','wP','wP'],
        ['wR','wN','wB','wQ','wK','wB','wN','wR'],
    ]

pc  = lambda p: p[0] if p else None
pt  = lambda p: p[1] if p else None
opp = lambda c: 'b' if c=='w' else 'w'
ib  = lambda r,c: 0<=r<8 and 0<=c<8

def pawn_moves(board,r,c,turn,ep):
    moves=[];  d=-1 if turn=='w' else 1;  sr=6 if turn=='w' else 1
    if ib(r+d,c) and not board[r+d][c]:
        moves.append((r+d,c,''))
        if r==sr and not board[r+2*d][c]: moves.append((r+2*d,c,''))
    for dc in (-1,1):
        nr,nc = r+d,c+dc
        if ib(nr,nc):
            if board[nr][nc] and pc(board[nr][nc])==opp(turn): moves.append((nr,nc,''))
            if ep and ep==(nr,nc): moves.append((nr,nc,'ep'))
    return moves

def slide_moves(board,r,c,dirs,turn):
    moves=[]
    for dr,dc in dirs:
        nr,nc = r+dr,c+dc
        while ib(nr,nc):
            if board[nr][nc]:
                if pc(board[nr][nc])!=turn: moves.append((nr,nc,''))
                break
            moves.append((nr,nc,''));  nr+=dr;  nc+=dc
    return moves

def knight_moves(board,r,c,turn):
    return [(nr,nc,'') for dr,dc in[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
            if ib(nr:=r+dr, nc:=c+dc) and pc(board[nr][nc])!=turn]

def king_basic(board,r,c,turn):
    return [(nr,nc,'') for dr,dc in[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            if ib(nr:=r+dr, nc:=c+dc) and pc(board[nr][nc])!=turn]

def is_attacked(board,r,c,by):
    for dr,dc in[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1),
                 (-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        nr,nc = r+dr,c+dc
        if ib(nr,nc):
            p=board[nr][nc]
            if p and pc(p)==by:
                t=pt(p)
                if t=='K' and abs(dr)<=1 and abs(dc)<=1: return True
                if t=='N' and (abs(dr),abs(dc)) in[(2,1),(1,2)]: return True
                pd=1 if by=='w' else -1
                if t=='P' and dr==pd and abs(dc)==1: return True
    for dirs,types in [([(-1,0),(1,0),(0,-1),(0,1)],('R','Q')),([ (-1,-1),(-1,1),(1,-1),(1,1)],('B','Q'))]:
        for dr,dc in dirs:
            nr,nc = r+dr,c+dc
            while ib(nr,nc):
                p=board[nr][nc]
                if p:
                    if pc(p)==by and pt(p) in types: return True
                    break
                nr+=dr;  nc+=dc
    return False

def find_king(board,color):
    for r in range(8):
        for c in range(8):
            if board[r][c]==color+'K': return (r,c)

def in_check(board,turn):
    kr,kc=find_king(board,turn);  return is_attacked(board,kr,kc,opp(turn))

def apply_move(board,fr,fc,tr,tc,extra=''):
    nb=[row[:] for row in board];  piece=nb[fr][fc];  cap=nb[tr][tc]
    if extra=='ep': cap=nb[fr][tc];  nb[fr][tc]=None
    nb[tr][tc]=piece;  nb[fr][fc]=None
    if extra=='castleK': row=fr;  nb[row][5]=nb[row][7];  nb[row][7]=None
    if extra=='castleQ': row=fr;  nb[row][3]=nb[row][0];  nb[row][0]=None
    return nb,cap

def get_raw_moves(board,r,c,turn,ep,castling):
    p=board[r][c]
    if not p or pc(p)!=turn: return []
    t=pt(p)
    if t=='P': return pawn_moves(board,r,c,turn,ep)
    if t=='N': return knight_moves(board,r,c,turn)
    if t=='B': return slide_moves(board,r,c,[(-1,-1),(-1,1),(1,-1),(1,1)],turn)
    if t=='R': return slide_moves(board,r,c,[(0,1),(0,-1),(1,0),(-1,0)],turn)
    if t=='Q': return slide_moves(board,r,c,[(-1,-1),(-1,1),(1,-1),(1,1),(0,1),(0,-1),(1,0),(-1,0)],turn)
    if t=='K':
        moves=king_basic(board,r,c,turn);  row=7 if turn=='w' else 0
        if (castling.get(turn+'K') and not board[row][5] and not board[row][6]
                and not is_attacked(board,row,4,opp(turn))
                and not is_attacked(board,row,5,opp(turn))
                and not is_attacked(board,row,6,opp(turn))): moves.append((row,6,'castleK'))
        if (castling.get(turn+'Q') and not board[row][3] and not board[row][2] and not board[row][1]
                and not is_attacked(board,row,4,opp(turn))
                and not is_attacked(board,row,3,opp(turn))
                and not is_attacked(board,row,2,opp(turn))): moves.append((row,2,'castleQ'))
        return moves
    return []

def get_legal_moves(board,r,c,turn,ep,castling):
    return [(tr,tc,ex) for tr,tc,ex in get_raw_moves(board,r,c,turn,ep,castling)
            if not in_check(apply_move(board,r,c,tr,tc,ex)[0],turn)]

def all_legal_moves(board,turn,ep,castling):
    return [((r,c),m) for r in range(8) for c in range(8)
            if pc(board[r][c])==turn
            for m in get_legal_moves(board,r,c,turn,ep,castling)]


# ─────────────────────────────────────────────
#  CHESS SQUARE  (extends Rect, auto-registers)
# ─────────────────────────────────────────────

class ChessSquare(Rect):
    def __init__(self, row, col, base_color, bx, by, cell):
        self.row = row;  self.col = col
        self.base_color = base_color
        self.piece = None;  self.highlight = None
        x = bx + col*cell;  y = by + row*cell
        super().__init__(x, y, cell, cell, base_color,
                         auto_register=True, is_interactive=True)

    def set_highlight(self, mode):
        self.highlight = mode
        colors = {'selected': SEL_COLOR, 'hint': HINT_COLOR, 'check': CHECK_COLOR}
        self.color = self._handle_color(colors.get(mode, self.base_color))

    def reposition(self, bx, by, cell):
        """Update position and size to match new board geometry."""
        self.x = bx + self.col*cell;  self.y = by + self.row*cell
        self.w = self.h = self.base_w = self.base_h = float(cell)
        self.ox = self.x;  self.oy = self.y
        self._handle_kwargs()

    def update_canvas(self, canvas, cell):
        """Sync canvas item geometry, colour, and piece glyph."""
        if hasattr(self,'rect_id'):
            canvas.coords(self.rect_id, self.draw_x, self.draw_y,
                          self.draw_x+self.w, self.draw_y+self.h)
            canvas.itemconfig(self.rect_id, fill=self.color)
        if hasattr(self,'piece_id'):
            canvas.delete(self.piece_id);  del self.piece_id
        if self.piece:
            glyph = PIECES_UNICODE.get(self.piece,'?')
            fg = '#ffffff' if self.piece[0]=='w' else '#1a1a1a'
            self.piece_id = canvas.create_text(
                self.draw_x+cell/2, self.draw_y+cell/2+2,
                text=glyph, font=('Segoe UI Symbol', max(8, int(cell*0.58))),
                fill=fg, anchor='center')

    def draw(self, canvas, cell):
        super().draw(canvas)
        self.update_canvas(canvas, cell)


# ─────────────────────────────────────────────
#  CHESS GAME STATE
# ─────────────────────────────────────────────

class ChessGame:
    def __init__(self):
        self.board = init_board();  self.turn = 'w'
        self.selected = None;  self.valid_moves = []
        self.ep = None;  self.castling = {'wK':True,'wQ':True,'bK':True,'bQ':True}
        self.captured = [];  self.history = [];  self.board_history = []
        self.game_over = False;  self.status_msg = 'White to move'
        self.squares: list[list[ChessSquare]] = []

    def build_squares(self, bx, by, cell):
        for r in range(8):
            row=[]
            for c in range(8):
                base = LIGHT_SQ if (r+c)%2==0 else DARK_SQ
                sq = ChessSquare(r, c, base, bx, by, cell)
                row.append(sq)
            self.squares.append(row)

    def sync_pieces(self):
        for r in range(8):
            for c in range(8):
                self.squares[r][c].piece = self.board[r][c]

    def clear_highlights(self):
        for row in self.squares:
            for sq in row: sq.set_highlight(None)

    def apply_highlights(self):
        self.clear_highlights()
        kp = find_king(self.board, self.turn)
        if in_check(self.board, self.turn): self.squares[kp[0]][kp[1]].set_highlight('check')
        if self.selected:
            sr,sc = self.selected;  self.squares[sr][sc].set_highlight('selected')
            for tr,tc,_ in self.valid_moves: self.squares[tr][tc].set_highlight('hint')

    def select_square(self, r, c):
        if self.game_over: return
        sp = self.board[r][c]
        if self.selected:
            match = next((m for m in self.valid_moves if m[0]==r and m[1]==c), None)
            if match: self.execute_move(self.selected[0], self.selected[1], *match);  return
            if sp and pc(sp)==self.turn:
                self.selected = (r,c)
                self.valid_moves = get_legal_moves(self.board,r,c,self.turn,self.ep,self.castling)
                self.apply_highlights();  return
            self.selected = None;  self.valid_moves = [];  self.apply_highlights();  return
        if sp and pc(sp)==self.turn:
            self.selected = (r,c)
            self.valid_moves = get_legal_moves(self.board,r,c,self.turn,self.ep,self.castling)
            self.apply_highlights()

    def execute_move(self, fr, fc, tr, tc, ex):
        piece = self.board[fr][fc]
        self.board_history.append([row[:] for row in self.board])
        nb, cap = apply_move(self.board, fr, fc, tr, tc, ex)
        if pt(piece)=='P' and (tr==0 or tr==7): nb[tr][tc] = self.turn+'Q'
        new_ep = ((fr+tr)//2, fc) if pt(piece)=='P' and abs(tr-fr)==2 else None
        nc2 = dict(self.castling)
        if piece=='wK': nc2['wK']=nc2['wQ']=False
        if piece=='bK': nc2['bK']=nc2['bQ']=False
        if piece=='wR' and fc==7: nc2['wK']=False
        if piece=='wR' and fc==0: nc2['wQ']=False
        if piece=='bR' and fc==7: nc2['bK']=False
        if piece=='bR' and fc==0: nc2['bQ']=False
        if cap: self.captured.append(cap)
        self.history.append(self._to_alg(piece,fr,fc,tr,tc,ex,cap))
        self.board=nb;  self.ep=new_ep;  self.castling=nc2
        self.turn=opp(self.turn);  self.selected=None;  self.valid_moves=[]
        self.sync_pieces()
        rem = all_legal_moves(self.board, self.turn, self.ep, self.castling)
        if not rem:
            self.game_over = True
            if in_check(self.board, self.turn):
                w = 'White' if self.turn=='b' else 'Black'
                self.status_msg = f'{w} wins by checkmate!'
            else:
                self.status_msg = 'Stalemate — draw!'
        else:
            chk = ' — Check!' if in_check(self.board, self.turn) else ''
            self.status_msg = ('White' if self.turn=='w' else 'Black') + f' to move{chk}'
        self.apply_highlights()

    def undo(self):
        if not self.board_history: return
        self.board = self.board_history.pop();  self.turn = opp(self.turn)
        if self.history: self.history.pop()
        if self.captured: self.captured.pop()
        self.selected=None;  self.valid_moves=[];  self.game_over=False
        self.status_msg = ('White' if self.turn=='w' else 'Black') + ' to move'
        self.sync_pieces();  self.apply_highlights()

    def _to_alg(self, piece, fr, fc, tr, tc, ex, cap):
        files='abcdefgh'
        if ex=='castleK': return 'O-O'
        if ex=='castleQ': return 'O-O-O'
        t=pt(piece);  dest=files[tc]+str(8-tr)
        if t=='P': return (files[fc]+'x'+dest) if (cap or ex=='ep') else dest
        return t+('x' if cap else '')+dest

class Layout:
    SIDEBAR_FRAC = 0.27
    MARGIN_FRAC  = 0.035

    def __init__(self, w, h): self.recompute(w, h)

    def recompute(self, win_w, win_h):
        self.win_w = win_w;  self.win_h = win_h
        mg = max(10, int(min(win_w,win_h)*self.MARGIN_FRAC))
        self.mg = mg
        sidebar_w  = int(win_w * self.SIDEBAR_FRAC)
        board_avail_w = win_w - sidebar_w - mg*3
        board_avail_h = win_h - mg*2
        cell = max(20, min(board_avail_w, board_avail_h)//8)
        self.cell  = cell
        bw = bh    = cell*8
        self.bx    = mg + (board_avail_w - bw)//2
        self.by    = mg + (board_avail_h - bh)//2
        self.sx    = self.bx + bw + mg
        self.sy    = self.by
        self.sw    = win_w - self.sx - mg
        self.sh    = bh
        gap        = max(6, mg//2)
        self.gap   = gap
        self.status_h   = max(44, int(self.sh * 0.09))
        self.captured_h = max(44, int(self.sh * 0.12))
        self.history_h  = max(60, int(self.sh * 0.50))
        self.btn_h      = max(30, int(self.sh * 0.08))
        self.btn_w      = max(60, (self.sw - gap)//2)
        self.fs_lbl  = max(8,  int(cell*0.14))
        self.fs_stat = max(9,  int(cell*0.17))
        self.fs_hist = max(8,  int(cell*0.14))
        self.fs_btn  = max(8,  int(cell*0.16))
        self.fs_coord= max(7,  int(cell*0.13))
        self.fs_cap  = max(10, int(cell*0.22))


# ─────────────────────────────────────────────
#  WINDOW + CANVAS
# ─────────────────────────────────────────────

window = ttk.Window('Chess', 'darkly', size=(960, 700))
window.minsize(500, 400)

canvas = ttk.Canvas(window, background='#1e1e1e', highlightthickness=0)
canvas.pack(fill='both', expand=True)

ly   = Layout(960, 700)
game = ChessGame()
game.build_squares(ly.bx, ly.by, ly.cell)
game.sync_pieces()
game.apply_highlights()

# Sidebar Panel/Button objects — recreated on every resize
_sidebar_objs: list = []
_dyn_ids: list[int] = []

status_panel   = None
captured_panel = None
history_panel  = None
new_btn        = None
undo_btn       = None


# ─────────────────────────────────────────────
#  BUILD SIDEBAR OBJECTS
# ─────────────────────────────────────────────

def build_sidebar():
    global status_panel, captured_panel, history_panel, new_btn, undo_btn, _sidebar_objs

    # Deregister old sidebar objects
    for obj in _sidebar_objs:
        if obj in game_objects:         game_objects.remove(obj)
        if obj in interactive_objects:  interactive_objects.remove(obj)

    sx, sy, sw, sh = ly.sx, ly.sy, ly.sw, ly.sh
    gap = ly.gap
    y   = sy

    status_panel   = Panel(sx, y, sw, ly.status_h,   PANEL_COLOR, border_radius=10)
    y += ly.status_h + gap

    captured_panel = Panel(sx, y, sw, ly.captured_h, PANEL_COLOR, border_radius=10)
    y += ly.captured_h + gap

    history_panel  = Panel(sx, y, sw, ly.history_h,  PANEL_COLOR, border_radius=10)

    btn_y = sy + sh - ly.btn_h

    def on_new():
        global game
        for row in game.squares:
            for sq in row:
                if sq in game_objects:         game_objects.remove(sq)
                if sq in interactive_objects:  interactive_objects.remove(sq)
        game = ChessGame()
        game.build_squares(ly.bx, ly.by, ly.cell)
        game.sync_pieces();  game.apply_highlights()
        full_redraw()

    def on_undo(): game.undo()

    new_btn  = Button(sx,                  btn_y, ly.btn_w, ly.btn_h,
                      (70,130,80), 'New Game', on_new,
                      border_radius=8, font_size=ly.fs_btn)
    undo_btn = Button(sx + ly.btn_w + gap, btn_y, ly.btn_w, ly.btn_h,
                      (130,80,70), 'Undo', on_undo,
                      border_radius=8, font_size=ly.fs_btn)

    _sidebar_objs = [status_panel, captured_panel, history_panel, new_btn, undo_btn]


# ─────────────────────────────────────────────
#  FULL CANVAS REDRAW
# ─────────────────────────────────────────────

def full_redraw():
    canvas.delete('all')

    # Board squares
    for row in game.squares:
        for sq in row: sq.draw(canvas, ly.cell)

    # Sidebar
    for obj in _sidebar_objs: obj.draw(canvas)

    # Coordinate labels
    files_str = 'abcdefgh'
    fcs = ly.fs_coord
    for i in range(8):
        canvas.create_text(
            ly.bx + i*ly.cell + ly.cell//2, ly.by + ly.cell*8 + fcs + 2,
            text=files_str[i], font=('Arial', fcs), fill='#aaaaaa', anchor='center')
        canvas.create_text(
            ly.bx - fcs - 3, ly.by + i*ly.cell + ly.cell//2,
            text=str(8-i), font=('Arial', fcs), fill='#aaaaaa', anchor='center')


# ─────────────────────────────────────────────
#  INPUT HANDLING
# ─────────────────────────────────────────────

mouse_state = {'x':0,'y':0,'is_hold':False}

def handle_press_1(e):
    mouse_state.update(x=e.x, y=e.y, is_hold=True)

def handle_release_1(e):
    mouse_state['is_hold'] = False
    _handle_click(e.x, e.y)
    for obj in interactive_objects:
        if hasattr(obj,'release_click'): obj.release_click()

def handle_motion(e):
    for obj in interactive_objects:
        if hasattr(obj,'check_hover') and obj.check_hover(e.x, e.y):
            if hasattr(obj,'rect_id'):
                canvas.itemconfig(obj.rect_id, fill=obj.color)

def _handle_click(x, y):
    # Buttons first
    for obj in interactive_objects:
        if hasattr(obj,'handle_click') and hasattr(obj,'on_click'):
            if obj.handle_click(x, y): return
    # Board squares
    for row in game.squares:
        for sq in row:
            if sq.check_click(x, y, True):
                game.select_square(sq.row, sq.col);  return

window.bind('<ButtonPress-1>',   handle_press_1)
window.bind('<ButtonRelease-1>', handle_release_1)
window.bind('<B1-Motion>',       handle_motion)


# ─────────────────────────────────────────────
#  RESIZE HANDLER  (debounced)
# ─────────────────────────────────────────────

_resize_id = None

def on_configure(event):
    global _resize_id
    if _resize_id: window.after_cancel(_resize_id)
    _resize_id = window.after(80, _apply_resize, event.width, event.height)

def _apply_resize(w, h):
    global _resize_id
    _resize_id = None
    if w < 100 or h < 100: return

    ly.recompute(w, h)

    # Reposition every board square
    for row in game.squares:
        for sq in row: sq.reposition(ly.bx, ly.by, ly.cell)

    # Rebuild sidebar with new sizes
    build_sidebar()
    full_redraw()

canvas.bind('<Configure>', on_configure)


# ─────────────────────────────────────────────
#  GAME LOOP  — per-frame updates only
# ─────────────────────────────────────────────

def redraw_dynamic_text():
    global _dyn_ids
    for tid in _dyn_ids: canvas.delete(tid)
    _dyn_ids = []

    add = _dyn_ids.append
    sx, sy = ly.sx, ly.sy
    gap    = ly.gap
    fsl    = ly.fs_lbl
    fss    = ly.fs_stat
    fsh    = ly.fs_hist
    fsc    = ly.fs_cap

    # ── Status ──
    add(canvas.create_text(sx+10, sy+5, text='Status', anchor='nw',
                            font=('Arial', fsl), fill='#888888'))
    add(canvas.create_text(sx+10, sy+8+fsl, text=game.status_msg, anchor='nw',
                            font=('Arial', fss, 'bold'), fill='#eeeeee'))

    # ── Captured ──
    y_cap = sy + ly.status_h + gap
    add(canvas.create_text(sx+10, y_cap+5, text='Captured', anchor='nw',
                            font=('Arial', fsl), fill='#888888'))
    w_cap = ''.join(PIECES_UNICODE[p] for p in game.captured if p and pc(p)=='b')
    b_cap = ''.join(PIECES_UNICODE[p] for p in game.captured if p and pc(p)=='w')
    add(canvas.create_text(sx+8, y_cap+8+fsl,       text=w_cap, anchor='nw',
                            font=('Segoe UI Symbol', fsc), fill='#dddddd'))
    add(canvas.create_text(sx+8, y_cap+10+fsl+fsc,  text=b_cap, anchor='nw',
                            font=('Segoe UI Symbol', fsc), fill='#dddddd'))

    # ── Move history ──
    y_his = y_cap + ly.captured_h + gap
    add(canvas.create_text(sx+10, y_his+5, text='Move history', anchor='nw',
                            font=('Arial', fsl), fill='#888888'))
    line_h   = max(13, int(fsh*1.6))
    max_lines= max(1, (ly.history_h - 14 - fsl) // line_h)
    visible  = game.history[-(max_lines*2):]
    for i in range(0, len(visible), 2):
        num    = (len(game.history)-len(visible))//2 + i//2 + 1
        w_move = visible[i]
        b_move = visible[i+1] if i+1<len(visible) else ''
        line   = f'{num:>2}. {w_move:<7} {b_move}'
        add(canvas.create_text(sx+10, y_his+8+fsl+(i//2)*line_h, text=line,
                                anchor='nw', font=('Courier', fsh), fill='#cccccc'))


def game_loop():
    # Sync board square colours + glyphs
    for row in game.squares:
        for sq in row: sq.update_canvas(canvas, ly.cell)

    # Sync button colours (hover/press)
    for btn in [new_btn, undo_btn]:
        if btn and hasattr(btn,'rect_id'):
            canvas.itemconfig(btn.rect_id, fill=btn.color)

    redraw_dynamic_text()
    canvas.update()
    window.after(30, game_loop)


# ─────────────────────────────────────────────
#  STARTUP
# ─────────────────────────────────────────────

build_sidebar()
full_redraw()
game_loop()
window.mainloop()