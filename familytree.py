from enum import Enum
import csv
import codecs

class Sex(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

class MarriageStatus(Enum):
    MARRIED = 1
    DIVORCED = 2
    UNMARRIED = 3

class Person():
    def __init__(self, name, sex, alive):
        self.name = name
        self.sex = Sex.MALE
        self.alive = True
        
        if sex == '男':
            self.sex = Sex.MALE
        elif sex == '女':
            self.sex = Sex.FEMALE
        elif sex == '其他':
            self.sex = Sex.OTHER
        
        if alive == '在世':
            self.alive = True
        elif alive == '逝世':
            self.alive = False

class Family():
    def __init__(self):
        self.biological_father = None
        self.biological_mother = None
        self.marriage_status = 'married'
        self.marriage_comment = ''
        self.children = []

    def set_marriage_status(self, marriage_status):
        if marriage_status == '結婚':
            self.marriage_status = MarriageStatus.MARRIED
        elif marriage_status == '離婚':
            self.marriage_status = MarriageStatus.DIVORCED
        elif marriage_status == '未婚':
            self.marriage_status = MarriageStatus.UNMARRIED

class Relation():
    def __init__(self):
        self.subject = None
        self.target = None
        self.comment = ''

class FamilyTreeDatabase():
    def __init__(self):
        self.people = dict()
        self.families = []
        self.relations = []

    def read_csv_files(self, people_csv_filename, families_csv_filename, relations_csv_filename):
        self.people.clear()
        self.families.clear()
        self.relations.clear()

        # People
        with codecs.open(people_csv_filename, 'r', 'utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Check if the name already exists.
                if row['人名'] in self.people:
                    continue
                
                person = Person(row['人名'], row['性別'], row['在世'])
                self.people[person.name] = person
        
        # Families
        with codecs.open(families_csv_filename, 'r', 'utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                family = Family()
                family.biological_father = self.people[row['生父']]
                family.biological_mother = self.people[row['生母']]
                family.set_marriage_status(row['婚姻狀態'])
                family.marriage_comment = row['婚姻備註']

                for child_key in ['子女' + str(i) for i in range(1, 11)]:
                    child_name = row[child_key]
                    if child_name != '':
                        family.children.append(self.people[child_name])
                
                self.families.append(family)

        # Relations
        with codecs.open(relations_csv_filename, 'r', 'utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                relation = Relation()
                relation.subject = self.people[row['主詞']]
                relation.target = self.people[row['受詞']]
                relation.comment = row['動作']
                self.relations.append(relation)
    
    def write_dot_file(self, dot_filename):
        with codecs.open(dot_filename, 'w', 'utf-8') as dot_file:
            dot_file.write('digraph {\n')
            dot_file.write('\toverlap = vpsc;\n')
            dot_file.write('\tsep = "+20,20";\n')
            dot_file.write('\tsplines = spline;\n')
            dot_file.write('\tnode [shape=box]\n')
            dot_file.write('\tedge [len=1.3]\n\n')

            # People
            for person_name, person in self.people.items():
                style_strings = []
                if person.sex == Sex.MALE:
                    if person.alive:
                        style_strings.append('color=blue')
                    else:
                        style_strings.append('color=blue4')
                elif person.sex == Sex.FEMALE:
                    if person.alive:
                        style_strings.append('color=red')
                    else:
                        style_strings.append('color=red4')
                elif person.sex == Sex.OTHER:
                    if person.alive:
                        style_strings.append('color=black')
                    else:
                        style_strings.append('color=gray')
                dot_file.write('\t' + person.name + '[' + ', '.join(style_strings) + ']' + ';\n')
            dot_file.write('\n')

            # Families
            for family in self.families:
                father_name = family.biological_father.name
                mother_name = family.biological_mother.name
                dot_file.write('\tsubgraph ' + father_name + mother_name + '{\n')
                dot_file.write('\t\tedge [dir=none]\n')
                dot_file.write('\t\trank=same;\n')
                dot_file.write('\t\t' + father_name + ';\n')
                dot_file.write('\t\t' + mother_name + ';\n')
                style_strings = []
                if family.marriage_status == MarriageStatus.DIVORCED:
                    style_strings.append('color=gray')
                elif family.marriage_status == MarriageStatus.UNMARRIED:
                    style_strings.append('color=pink')
                if family.marriage_comment != '':
                    style_strings.append('label="' + family.marriage_comment + '"')
                dot_file.write('\t\t' + father_name + ' -> ' + mother_name + '[' + ', '.join(style_strings) + ']' + ';\n')
                dot_file.write('\t}\n')
                marriage_title = father_name + mother_name + '婚姻'
                dot_file.write('\t' + marriage_title + '[label="", shape=circle];\n')
                dot_file.write('\t' + father_name + ' -> ' + marriage_title + ';\n')
                dot_file.write('\t' + mother_name + ' -> ' + marriage_title + ';\n')
                for child in family.children:
                    dot_file.write('\t' + marriage_title + ' -> ' + child.name + ';\n')
                dot_file.write('\n')
            dot_file.write('\n')

            # Relations
            for relation in self.relations:
                dot_file.write('\t' + relation.subject.name + ' -> ' + relation.target.name + '[label="' + relation.comment + '", style=dashed];\n')

            dot_file.write('}\n')

if __name__ == '__main__':
    family_tree_database = FamilyTreeDatabase()
    family_tree_database.read_csv_files('input/FamilyTree - People.csv', 'input/FamilyTree - Families.csv', 'input/FamilyTree - Relations.csv')
    family_tree_database.write_dot_file('output/FamilyTree.dot')
