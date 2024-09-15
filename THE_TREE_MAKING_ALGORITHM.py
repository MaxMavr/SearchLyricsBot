from vector_operation import calc_centvec, calc_delta_sqr_err, rounded_vec, word2vec, vec2word
from file_interface import take_unp_vecs_from_file, make_vec_file
from config import VEC_DIR, json
 
'''

vecs = [i[1] for i in take_unp_vecs_from_file()]
nodes = []
active_node_indexes = []


for vec_index in range(len(vecs)):
    node = {"left_node_index": None, "right_node_index": None, 
            "parent_node_index": None, "vec_index": vec_index}
    nodes.append(node)
    active_node_indexes.append(len(nodes) - 1)

while len(active_node_indexes) > 1:
    print(len(active_node_indexes))
    max_similarity = -1
    for i in range(len(active_node_indexes)):
        for j in range(i + 1, len(active_node_indexes)):
            left_node_index_temp = active_node_indexes[i]
            right_node_index_temp = active_node_indexes[j]
            left_vec_index = nodes[left_node_index_temp]["vec_index"]
            right_vec_index = nodes[right_node_index_temp]["vec_index"]
            similarity = calc_delta_sqr_err(vecs[left_vec_index], vecs[vec_index])
            if similarity > max_similarity:
                max_similarity = similarity
                left_node_index = left_node_index_temp
                right_node_index = right_node_index_temp

    active_node_indexes.remove(left_node_index)
    active_node_indexes.remove(right_node_index)

    average_vec = calc_centvec(vecs[nodes[left_node_index]["vec_index"]], vecs[nodes[right_node_index]["vec_index"]])
    vecs.append(average_vec)
    parent_node = {"left_node_index": left_node_index, "right_node_index": right_node_index, 
                   "parent_node_index": None, "vec_index": len(vecs) - 1}
    nodes.append(parent_node)
    nodes[left_node_index]["parent_node_index"] = len(nodes) - 1
    nodes[right_node_index]["parent_node_index"] = len(nodes) - 1
    active_node_indexes.append(len(nodes) - 1)

make_vec_file(f"{VEC_DIR}/vectors1", vecs)
make_vec_file(f"{VEC_DIR}/nodes1", nodes)

'''
# PHASALO ON : 

def take_vecs_from_vectors1():
    with open(f"{VEC_DIR}/vectors1.json", 'r', encoding="utf-8") as file:
        return json.load(file)
    
def take_nodes_from_nodes1():
    with open(f"{VEC_DIR}/nodes1.json", 'r', encoding="utf-8") as file:
        return json.load(file)

# : PHASALO OFF
vecs = take_vecs_from_vectors1()
nodes = take_nodes_from_nodes1()


word_2_find = "хер"

vec_2_find = word2vec(word_2_find)

current_node_index = len(nodes)-1
current_node = nodes[current_node_index]

while current_node["left_node_index"] is not None or \
      current_node["right_node_index"] is not None:

    if current_node["left_node_index"] is None:
        left_word = "none"
        right_node = nodes[current_node["right_node_index"]]
        right_vec_index = right_node["vec_index"]
        right_vec = vecs[right_vec_index]
        right_word = vec2word(rounded_vec(right_vec))
        current_node_index = right_vec_index
        
        left_similarity = "pohuy"
        right_similarity = "pohuy"

    elif current_node["right_node_index"] is None:
        left_node = nodes[current_node["left_node_index"]]
        left_vec_index = left_node["vec_index"]
        left_vec = vecs[left_vec_index]
        left_word = vec2word(rounded_vec(left_vec))
        right_word = "none"
        current_node_index = left_vec_index

        left_similarity = "pohuy"
        right_similarity = "pohuy"
    else:
        left_node = nodes[current_node["left_node_index"]]
        left_vec_index = left_node["vec_index"]
        left_vec = vecs[left_vec_index]
        left_word = vec2word(rounded_vec(left_vec))
        
        right_node = nodes[current_node["right_node_index"]]
        right_vec_index = right_node["vec_index"]
        right_vec = vecs[right_vec_index]
        right_word = vec2word(rounded_vec(right_vec))

        left_similarity = calc_delta_sqr_err(vec_2_find, left_vec)
        right_similarity = calc_delta_sqr_err(vec_2_find, right_vec)
        
        if left_similarity > right_similarity:
            current_node_index = left_vec_index
        else:
            current_node_index = right_vec_index

    current_node = nodes[current_node_index]
    current_vec_index = current_node["vec_index"]
    current_vec = vecs[current_vec_index]
    current_word = vec2word(rounded_vec(current_vec))
    print(f"{word_2_find.ljust(10)}: {left_word.ljust(10)} vs {right_word.ljust(10)}")
    print(f"          {str(left_similarity).ljust(10)} vs {str(right_similarity).ljust(10)}")
    print(f"  Winner: {current_word.ljust(10)}")

