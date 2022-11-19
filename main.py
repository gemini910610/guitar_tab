import os
import msvcrt
import json


class Tab:
    def __init__(self):
        self.data = [[['', '', '', '', '', '']]]
        self.load()

        self.current_section = 0
        self.current_node = 0
        self.current_character = ''
        self.history = ''

    def get_section(self, section_index=None):
        if section_index is None:
            section_index = self.current_section
        return self.data[section_index]

    def get_node(self, section_index=None, node_index=None):
        if section_index is None:
            section_index = self.current_section
        if node_index is None:
            node_index = self.current_node
        return self.data[section_index][node_index]

    def insert_section_after(self, section_index=None):
        if section_index is None:
            section_index = self.current_section
        self.data.insert(section_index + 1, [['', '', '', '', '', '']])

    def insert_node_after(self, section_index=None, node_index=None):
        if section_index is None:
            section_index = self.current_section
        if node_index is None:
            node_index = self.current_node
        self.data[section_index].insert(node_index + 1, ['', '', '', '', '', ''])

    def remove_section(self, section_index=None):
        if section_index is None:
            section_index = self.current_section
        self.data.pop(section_index)

    def remove_node(self, section_index=None, node_index=None):
        if section_index is None:
            section_index = self.current_section
        if node_index is None:
            node_index = self.current_node
        self.data[section_index].pop(node_index)

    @property
    def section_count(self):
        return len(self.data)

    def get_node_count(self, section_index=None):
        if section_index is None:
            section_index = self.current_section
        return len(self.data[section_index])

    def to_str(self, mode = None):
        top = ''
        line = ['|', '|', '|', '|', '|', '|']
        for section_num in range(len(self.data)):
            for i in range(6):
                line[i] += ('─' if mode != 'output' else '-')
            if section_num + 1 < 100:
                top += f'{section_num + 1}'
            else:
                top += f'{section_num + 1 - 100 :>02}'
            if section_num + 1 < 10:
                top += ' '
            section = self.get_section(section_num)
            for node_num in range(len(section)):
                node = section[node_num]
                length = len(max(node, key=lambda element: len(element)))
                if length == 0:
                    length = 1
                for i in range(6):
                    if node[i] != '':
                        line[i] += node[i]
                    line[i] += ('─' if mode != 'output' else '-') * (length - len(node[i]) + 1)
                if (
                    section_num == self.current_section
                    and node_num == self.current_node
                    and mode != 'output'
                ):
                    top += 'v' + ' ' * length
                else:
                    top += ' ' * (length + 1)
            for i in range(6):
                line[i] += '|'
        top += ' '
        return [top, line]
    
    def output(self, mode = None):
        top, line = self.to_str(mode)
        ls = []
        for l in line:
            ls.append(l.split('|')[1:-1])
        t = []
        for l in ls[0]:
            t.append(top[:len(l) + 1])
            top = top[len(l) + 1:]
        length = 0
        result = (['', '┌', '├', '├', '├', '├', '└'] if mode != 'output' else [' ', ' +', ' |', ' |', ' |', ' |', ' +'])
        output = ''
        for i in range(len(t)):
            result[0] += t[i]
            for j in range(6):
                result[j+1] += ls[j][i]
            length += len(t[i])
            if length > 100:
                output += f'{result[0]}\n'
                output += f'{result[1]}' + ('┐' if mode != 'output' else '+') + '\n'
                output += f'{result[2]}' + ('┤' if mode != 'output' else '|') + '\n'
                output += f'{result[3]}' + ('┤' if mode != 'output' else '|') + '\n'
                output += f'{result[4]}' + ('┤' if mode != 'output' else '|') + '\n'
                output += f'{result[5]}' + ('┤' if mode != 'output' else '|') + '\n'
                output += f'{result[6]}' + ('┘' if mode != 'output' else '+') + '\n'
                output += '\n'
                length = 0
                result = (['', '┌', '├', '├', '├', '├', '└'] if mode != 'output' else [' ', ' +', ' |', ' |', ' |', ' |', ' +'])
            elif i != len(t) - 1:
                result[1] += ('┬' if mode != 'output' else '+')
                result[2] += ('┼' if mode != 'output' else '|')
                result[3] += ('┼' if mode != 'output' else '|')
                result[4] += ('┼' if mode != 'output' else '|')
                result[5] += ('┼' if mode != 'output' else '|')
                result[6] += ('┴' if mode != 'output' else '+')
        if result != (['', '┌', '├', '├', '├', '├', '└'] if mode != 'output' else [' ', ' +', ' |', ' |', ' |', ' |', ' +']):
            output += f'{result[0]}\n'
            output += f'{result[1]}' + ('╖' if mode != 'output' else '+') + '\n'
            output += f'{result[2]}' + ('╢' if mode != 'output' else '|') + '\n'
            output += f'{result[3]}' + ('╢' if mode != 'output' else '|') + '\n'
            output += f'{result[4]}' + ('╢' if mode != 'output' else '|') + '\n'
            output += f'{result[5]}' + ('╢' if mode != 'output' else '|') + '\n'
            output += f'{result[6]}' + ('╜' if mode != 'output' else '+') + '\n'
            output += '\n'
        return output

    def print(self, refresh = True):
        os.system('cls')
        if refresh:
            self.history = self.output()
        print(self.history, end='')
        print(f'+ {self.current_character}')

    def save(self):
        with open('tab.json', 'w') as file:
            file.write(json.dumps(self.data))

    def load(self):
        if os.path.exists('tab.json'):
            with open('tab.json') as file:
                self.data = json.load(file)


def convert_to_node(input_num):
    return {
        -5: [5, 0],
        -4: [5, 1],
        -3: [5, 3],
        -2: [4, 0],
        -1: [4, 2],
        0: [4, 3],
        1: [3, 0],
        2: [3, 2],
        3: [3, 3],
        4: [2, 0],
        5: [2, 2],
        6: [1, 0],
        7: [1, 1],
        8: [1, 3],
        9: [0, 0],
        10: [0, 1],
        11: [0, 3],
        12: [0, 5],
        13: [0, 7],
        14: [0, 8],
        15: [0, 10],
        16: [0, 12],
        17: [0, 13],
        18: [0, 15],
        19: [0, 17],
        20: [0, 19],
        21: [0, 20],
    }[input_num]


tab = Tab()
tab.print()

while True:
    if msvcrt.kbhit():
        refresh = True
        message = ''
        character = msvcrt.getch()
        if character == b'\x00' or character == b'\xe0':
            character = msvcrt.getch()
            match character:
                case b'M':  # right
                    if tab.current_node < tab.get_node_count() - 1:
                        tab.current_node += 1
                    elif tab.current_section < tab.section_count - 1:
                        tab.current_node = 0
                        tab.current_section += 1
                case b'K':  # left
                    if tab.current_node > 0:
                        tab.current_node -= 1
                    elif tab.current_section > 0:
                        tab.current_section -= 1
                        tab.current_node = tab.get_node_count() - 1
                case b'S':  # delete
                    tab.print(False)
                    remove = input('> ')
                    if remove == '':
                        if not (
                            tab.current_node == 0
                            and tab.current_section == 0
                            and tab.section_count == 1
                            and tab.get_node_count(0) == 1
                        ):
                            tab.remove_node()
                            if tab.current_node != 0:
                                tab.current_node -= 1
                            if tab.get_node_count() == 0:
                                tab.remove_section()
                                if tab.current_section > tab.section_count - 1:
                                    tab.current_section -= 1
                                tab.current_node = tab.get_node_count() - 1
                        elif tab.get_node(0, 0) != ['', '', '', '', '', '']:
                            tab.data[0][0] = ['', '', '', '', '', '']
                    elif '1' <= remove <= '6':
                        tab.get_node()[int(remove) - 1] = ''
                case b'R':  # insert
                    tab.insert_node_after(node_index=tab.current_node - 1)
        elif character == b'\x08':  # backspace
            refresh = False
            if tab.current_character != b'':
                tab.current_character = tab.current_character[:-1]
        elif character == b'\x1b':  # esc
            tab.current_section = tab.section_count - 1
            tab.current_node = tab.get_node_count() - 1
        elif character == b'\x13':  # Ctrl + S
            refresh = False
            tab.save()
            message = 'save as tab.json'
        elif character == b'\x0f': # Ctrl + O
            refresh = False
            with open('tab.txt', 'w') as file:
                file.write(tab.output('output'))
            message = 'save as tab.txt'
        elif character == b' ':
            if tab.current_character != '':
                line, number = convert_to_node(int(tab.current_character))
                tab.get_node()[line] = str(number)
            tab.insert_node_after()
            tab.current_node += 1
            tab.current_character = ''
        elif character == b'\r':  # enter
            if tab.current_character != '':
                line, number = convert_to_node(int(tab.current_character))
                tab.get_node()[line] = str(number)
                tab.current_character = ''
            else:
                if (
                    tab.get_node() == ['', '', '', '', '', '']
                    and tab.current_node == tab.get_node_count() - 1
                    and tab.get_node_count() != 1
                ):
                    tab.remove_node()
                tab.current_node = 0
                tab.insert_section_after()
                tab.current_section += 1
        elif b'0' <= character <= b'9' or character == b'-':
            refresh = False
            tab.current_character += character.decode('utf-8')
        tab.print(refresh)
        if message != '':
            print(message)
