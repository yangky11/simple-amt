import argparse, json
import pdb

import os
import simpleamt
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
    parser.add_argument('--hit_properties_file', type=argparse.FileType('r'))
    parser.add_argument('--url', type=str)
    parser.add_argument('--num', type=int)
    args = parser.parse_args()

    mtc = simpleamt.get_mturk_connection_from_args(args)

    hit_properties = json.load(args.hit_properties_file)
    hit_properties['Reward'] = str(hit_properties['Reward'])
    simpleamt.setup_qualifications(hit_properties, mtc)
    
    frame_height = hit_properties.pop('FrameHeight')

    external_question = '''
    <ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
        <ExternalURL>%s</ExternalURL>
        <FrameHeight>%d</FrameHeight>
    </ExternalQuestion>
    ''' % (args.url, frame_height)
    hit_properties['Question'] = external_question

    if args.hit_ids_file is None:
        print('Need to input a hit_ids_file')
        sys.exit()
    if os.path.isfile(args.hit_ids_file):
        print('hit_ids_file already exists')
        sys.exit()

    pdb.set_trace()
    with open(args.hit_ids_file, 'w') as hit_ids_file:
        for i in range(args.num):
            launched = False
            while not launched:
                try:
                    boto_hit = mtc.create_hit(**hit_properties)
                    launched = True
                except Exception as e:
                    print(e)
            hit_id = boto_hit['HIT']['HITId']
            hit_ids_file.write('%s\n' % hit_id)
            print('Launched HIT ID: %s, %d' % (hit_id, i + 1))


