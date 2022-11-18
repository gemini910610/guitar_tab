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

    def to_str(self):
        top = ''
        line = ['|', '|', '|', '|', '|', '|']
        for section_num in range(len(self.data)):
            for i in range(6):
                line[i] += '-'
            top += f'{section_num + 1} '
            section = self.get_section(section_num)
            for node_num in range(len(section)):
                node = section[node_num]
                length = len(max(node, key=lambda element: len(element)))
                if length == 0:
                    length = 1
                for i in range(6):
                    if node[i] != '':
                        line[i] += node[i]
                    line[i] += '-' * (length - len(node[i]) + 1)
                if (
                    section_num == self.current_section
                    and node_num == self.current_node
                ):
                    top += 'v' + ' ' * length
                else:
                    top += ' ' * (length + 1)
            for i in range(6):
                line[i] += '|'
        return [top, line]

    def print(self):
        os.system('cls')
        top, line = self.to_str()
        print(top)
        for i in range(6):
            print(line[i])
        print(f'+ {self.current_character}')

    def save(self):
        with open('tab.json', 'w') as file:
            file.write(json.dumps(self.data))

    def load(self):
        if os.path.exists('tab.json'):
            with open('tab.json') as file:
                self.data = json.load(file)


def convert_to_node(input_num):
    return [
        [4, 3],
        [3, 0],
        [3, 2],
        [3, 3],
        [2, 0],
        [2, 2],
        [1, 0],
        [1, 1],
        [1, 3],
        [0, 0],
        [0, 1],
        [0, 3],
        [0, 5],
        [0, 7],
        [0, 8],
        [0, 10],
        [0, 12],
        [0, 13],
        [0, 15],
        [0, 17],
        [0, 19],
        [0, 20],
    ][input_num - 1]


tab = Tab()
tab.print()

while True:
    if msvcrt.kbhit():
        character = msvcrt.getch()
        if character == b'\x00':
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
                    tab.print()
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
            if tab.current_character != b'':
                tab.current_character = tab.current_character[:-1]
        elif character == b'\x1b':  # esc
            tab.current_section = tab.section_count - 1
            tab.current_node = tab.get_node_count() - 1
        elif character == b'\x13':  # Ctrl + S
            tab.save()
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
                if tab.get_node() == ['', '', '', '', '', ''] and tab.current_node == tab.get_node_count() - 1 and tab.get_node_count() != 1:
                    tab.remove_node()
                tab.current_node = 0
                tab.insert_section_after()
                tab.current_section += 1
        elif b'0' <= character <= b'9':
            tab.current_character += character.decode('utf-8')
        tab.print()
