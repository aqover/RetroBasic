terminal = ['id', 'line_num', 'const', 'IF', 'PRINT', 'GOTO', 'STOP', '+', '-', '<', '=', 'EOF']
startSymbol = 'pgm'

class BCode:
	"""docstring for BCode"""
	def __init__(self):
		self.bcode_format = {
			'line_num': '10 {}',
			'id': '11 {}',
			'const': '12 {}',
			'IF': '13 0',
			'GOTO': '14 {}',
			'PRINT': '15 0',
			'STOP': '16 0',
			'+': '17 1',
			'-': '17 2',
			'<': '17 3',
			'=': '17 4',
		}

		self.matcher = [
			('const', self._ck3),
			('id', self._ck1),
			('line_num', self._ck2),
			('IF', self._ck4),
			('GOTO', self._ck6),
			('PRINT', self._ck5),
			('STOP', self._ck7),
			('+', self._ck8),
			('-', self._ck9),
			('<', self._ck10),
			('=', self._ck11),
		]

	def GetMatcher(self):
		return self.matcher

	def GetFormat(self):
		return self.bcode_format

	def GetToken(self, idx, txt, is_line_num = 0):
		if (idx == 0 or is_line_num) and self._ck1(txt):
			return ('line_num', int(txt))
		else:
			for ck in self.matcher[0:]:
				(res, vaule) = ck[1](txt)
				if res:
					return (ck[0], vaule)
					break
		return (None, None)

	def _ck1(self, x):
		res = False if len(x) > 1 else 'A' <= x <= 'Z'
		if res:
			return (res, ord(x) - ord('A') + 1)
		return (False, None)

	def _ck2(self, x):
		try:
			x = int(x)
		except:
			return (False, None)
		else:
			return (0 <= x <= 1000, x)
		return (False, None)
	
	def _ck3(self, x):
		try:
			x = int(x)
		except:
			return (False, None)
		else:
			return (0 <= x <= 1000, x)
		return (False, None)

	def _ck4(self, x):
		return ('IF' == x, 'IF')
	def _ck5(self, x):
		return ('PRINT' == x, 'PRINT')
	def _ck6(self, x):
		return ('GOTO' == x, 'GOTO')
	def _ck7(self, x):
		return ('STOP' == x, 'STOP')
	def _ck8(self, x):
		return ('+' == x, '+')
	def _ck9(self, x):
		return ('-' == x, '-')
	def _ck10(self, x):
		return ('<' == x, '<')
	def _ck11(self, x):
		return ('=' == x, '=')


grammar_rule = {
	'pgm': [['line', 'pgm'], ['EMPTY']],
	'line': [['line_num', 'stmt']],
	'stmt': [['asgmt'], ['if'], ['print'], ['goto'], ['stop']],
	'asgmt': [['id', '=', 'exp']],
	'exp': [['term', 'exp2']],
	'exp2': [['+', 'term'], ['-', 'term'], ['EMPTY']],
	'term': [['id'], ['const']],
	'if': [['IF', 'cond', 'line_num']],
	'cond': [['term', 'cond2']],
	'cond2': [['<', 'term'], ['=', 'term']],
	'print': [['PRINT', 'id']],
	'goto': [['GOTO', 'line_num']],
	'stop': [['STOP']],
}

first_set = {
	'pgm': set(['line_num']),
	'line': set(['line_num']),
	'stmt': set(['id', 'IF', 'PRINT', 'GOTO', 'STOP']),
	'asgmt': set(['id']),
	'exp': set(['id', 'const']),
	'exp2': set(['+', '-', 'EMPTY']),
	'term': set(['id', 'const']),
	'if': set(['IF']),
	'cond': set(['id', 'const']),
	'cond2': set(['<', '=']),
	'print': set(['PRINT']),
	'goto': set(['GOTO']),
	'stop': set(['STOP']),
}

follow_set = {
	'pgm': set(['EOF']),
	'line': set(['line_num', 'EOF']),
	'stmt': set(['line_num', 'EOF']),
	'asgmt': set(['line_num', 'EOF']),
	'exp': set(['line_num', 'EOF']),
	'exp2': set(['line_num', 'EOF']),
	'term': set(['+', '-', '<', '=', 'id', 'const', 'line_num', 'EOF']),
	'if': set(['line_num', 'EOF']),
	'cond': set(['line_num']),
	'cond2': set(['line_num']),
	'print': set(['line_num', 'EOF']),
	'goto': set(['line_num', 'EOF']),
	'stop': set(['line_num', 'EOF']),
}

paring_table = {
	'pgm': 		[-1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1],
	'line': 	[-1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	'stmt': 	[3, -1, -1, 4, 5, 6, 7, -1, -1, -1, -1, -1],
	'asgmt': 	[8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	'exp': 		[9, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	'exp2': 	[-1, 12, -1, -1, -1, -1, -1, 10, 11, -1, -1, 23],
	'term': 	[13, -1, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	'if': 		[-1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1],
	'cond': 	[16, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	'cond2': 	[-1, -1, -1, -1, -1, -1, -1, -1, -1, 17, 18, -1],
	'print': 	[-1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1],
	'goto': 	[-1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1],
	'stop': 	[-1, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1,- 1],
}