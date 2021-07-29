import os
import uuid
import json

template_directory = './data/template/'
target_directory = './output/'

def read_file(filename):
    with open(filename) as f:
        contents = f.readlines()
    return ('').join(contents)

def write_file(filename, content):
    file2 = open(filename, "w+")
    file2.write(content)
    file2.close()

def main():
    os.mkdir(target_directory)

    questions = json.loads(read_file('data/bia.json'))

    question_types = [
        '1000',
        '1110',
        '1001',
        '1100',
        '1101',
        '1010',
        '1011',
        '0100',
        '0110',
        '0111',
        '0101',
        '0010',
        '0011',
        '0001',
    ]

    question_templates = {}

    for filename in os.listdir(template_directory):
        if filename.endswith(".xml"):
            template = read_file(template_directory + filename)
            #print(template)
        for qt in question_types:
            if qt in template:
                question_templates[qt] = template

    # produce question xmls
    q_ids = []
    for i, q in enumerate(questions):
        question = q[0]
        question_type = str(q[1]) + str(q[3]) + str(q[5]) + str(q[7])
        answer1 = q[2]
        answer2 = q[4]
        answer3 = q[6]
        answer4 = q[8]

        question_template = question_templates[question_type] + ""
        question_template = question_template.replace(question_type, "Question " + str(i + 1))
        question_template = question_template.replace('Template_Question', question)
        question_template = question_template.replace('Template_Answer0', answer1)
        question_template = question_template.replace('Template_Answer1', answer2)
        question_template = question_template.replace('Template_Answer2', answer3)
        question_template = question_template.replace('Template_Answer3', answer4)

        filename = 'id' + str(uuid.uuid4())
        write_file(target_directory + str(filename) + ".xml", question_template)
        q_ids.append(filename)

    # produce meta data xml
    metadata = read_file(template_directory + 'idTest15cffd81-7a01-4cf2-976a-5fd0f6871102.xml')
    metadata = metadata.replace('idc148246b-3867-4d76-b523-19b4e4f878b2', 'idc' + str(uuid.uuid4()))
    metadata = metadata.replace('id7c4571a3-59d5-4a21-ac27-e20d40b9031f', 'idc' + str(uuid.uuid4()))
    test_id = 'idTest' + str(uuid.uuid4())
    metadata = metadata.replace('idTest15cffd81-7a01-4cf2-976a-5fd0f6871102', test_id)
    assessments_refs = ''.join(['<assessmentItemRef identifier="' + str(q_id) + '" href="' + str(q_id) + '.xml" fixed="false" />' for q_id in q_ids])
    metadata = metadata.replace('##ASSESSMENT_REFS##', assessments_refs)
    write_file(target_directory + test_id + '.xml', metadata)

    # produce manifest
    manifest = read_file(template_directory + 'imsmanifest.xml')
    #manifest = manifest.replace('idTest15cffd81_7a01_4cf2_976a_5fd0f6871102_manifest', test_id + '_manifest')
    manifest = manifest.replace('idTest15cffd81-7a01-4cf2-976a-5fd0f6871102', test_id)
    #                           'idTest15cffd81-7a01-4cf2-976a-5fd0f6871102'

    all_dependencies = ''.join(['<dependency identifierref="' + str(q_id) + '" />' for q_id in q_ids])
    manifest = manifest.replace('##ALL_DEPENDENCIES##', all_dependencies)

    all_resources = ''.join(['<resource identifier="' + str(q_id) + '" type="imsqti_item_xmlv2p1" href="' + str(q_id) + '.xml"><file href="' + str(q_id) + '.xml" /></resource>' for q_id in q_ids])
    manifest = manifest.replace('##ALL_RESOURCES##', all_resources)
    write_file(target_directory + 'imsmanifest.xml', manifest)


if __name__ == '__main__':
    main()

