import argparse, numpy as np
parser = argparse.ArgumentParser()

def get_str_states(rr,bb,f):
    return (f-1)*500+bb*30+rr+2

def decode(path_states,path_value_policy):
    mdp=""
    states = open(path_states).read().strip().split("\n")
    states = np.array(list(map(lambda x: x.split(), states)), dtype=str)

    with open(path_value_policy, 'r') as f:
        lines = f.readlines()

    value_policy=np.zeros((len(lines),2))
    for i in range(len(lines)):
        #if lines[i]=="\n":
        #    continue
        temp=np.array(lines[i].strip().split())
        #print(temp[2][3][3]," ",i)
        value_policy[i][0]=float(temp[0])
        value_policy[i][1]=float(temp[1])
        
        #print(value_policy[i]," ",i)
    
    

    for i in range(len(states)):
        bb=int(int(states[i][0])/100)
        rr=int(states[i][0])%100
        j=get_str_states(rr,bb,1)
        mdp+=f"{states[i][0]} {int(value_policy[j][1])} {value_policy[j][0]}"
        if(i!=len(states)-1):
            mdp+=f"\n"
    print(mdp)
    

if __name__ == "__main__":
    parser.add_argument("--states", type=str)
    parser.add_argument("--value-policy", type=str)
    args = parser.parse_args()
    decode(args.states,args.value_policy)

    
    #python3 decoder.py --value-policy /host/Assignment2/code/verify_attt_planner --states /host/Assignment2/code/data/cricket/cricket_state_list.txt 