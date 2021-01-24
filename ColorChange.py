
import json
import csv

# Damage class ID: 1 is no damage, 2 is physical, 3 is special
# Types: use types.csv

move_name_dict = {}

with open('moves.csv', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        move_name_dict[row['identifier']] = row
        no_hyphens = row['identifier'].replace('-','')
        move_name_dict[no_hyphens] = row

print(move_name_dict)
weakness_dict = {}
with open('type_efficacy.csv', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row['damage_factor'] == '200':
            if row['target_type_id'] in weakness_dict:
                weakness_dict[row['target_type_id']].append(row['damage_type_id'])
            else:
                weakness_dict[row['target_type_id']] = [row['damage_type_id']]


print(weakness_dict)
with open('gen8cap-1500.json') as json_file:
    usage_dict = json.load(json_file)
    print(usage_dict)

for pokemon in usage_dict['data']:
    usage_total = 0
    for ability in usage_dict['data'][pokemon]['Abilities']:
        usage_total += usage_dict['data'][pokemon]['Abilities'][ability]
    # print(usage_total)
    move_pairing_dict = {}
    for move in usage_dict['data'][pokemon]['Moves']:
        # skip non-damaging moves
        #print(move)
        if move not in move_name_dict:
            print("missing move:", move)
            continue
        if move == '' or move_name_dict[move]['damage_class_id'] == '1':
            continue
        move_type = move_name_dict[move]['type_id']
        move_pairing_dict[move] = {'usage': usage_dict['data'][pokemon]['Moves'][move],
                                   'moves': {}}
        type_weaknesses = weakness_dict[move_type]
        for move2 in usage_dict['data'][pokemon]['Moves']:
            if move2 not in move_name_dict:
                continue
            if move2 == '' or move_name_dict[move2]['damage_class_id'] == '1':
                continue
            if move_name_dict[move2]['type_id'] in type_weaknesses:
                # print(f"Absorbing {move} will make you weak to {move2} from {pokemon}")
                move_pairing_dict[move]['moves'][move2] = usage_dict['data'][pokemon]['Moves'][move2]
    print(pokemon, move_pairing_dict)
    for absorbed_move in move_pairing_dict:
        a_move_usage = move_pairing_dict[absorbed_move]['usage'] / usage_total
        has_none_chance = 1.0
        for super_move in move_pairing_dict[absorbed_move]['moves']:
            if super_move == absorbed_move:
                has_none_chance = 0
                break
            doesnt_have_probability = 1.0 - (move_pairing_dict[absorbed_move]['moves'][super_move]/usage_total)
            has_none_chance *= doesnt_have_probability

        print(f"There's a {has_none_chance} probability that {pokemon} won't have a move that's SE "
              f"after using {absorbed_move}")











