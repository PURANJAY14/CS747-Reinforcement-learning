import argparse, numpy as np
parser = argparse.ArgumentParser()

def get_str_states(rr,bb,f):
    return (f-1)*500+bb*30+rr+2

def encode(path_states,path_parametrs,q):
    # collect mdp data from maze
    states = open(path_states).read().strip().split("\n")
    states = np.array(list(map(lambda x: x.split(), states)), dtype=int)
    prob=np.zeros((7,7))
    with open(path_parametrs, 'r') as f:
        lines = f.readlines()
    
    temp=np.array(lines[1].strip().split())
    for j in range(1,len(temp)):
        prob[0][j-1]=float(temp[j])

    temp=np.array(lines[2].strip().split())
    for j in range(1,len(temp)):
        prob[1][j-1]=float(temp[j])

    temp=np.array(lines[3].strip().split())
    for j in range(1,len(temp)):
        prob[2][j-1]=float(temp[j])

    temp=np.array(lines[4].strip().split())
    for j in range(1,len(temp)):
        prob[4][j-1]=float(temp[j])

    temp=np.array(lines[5].strip().split())
    for j in range(1,len(temp)):
        prob[6][j-1]=float(temp[j])
    #prob = np.array(list(map(lambda x: x.split(), prob)), dtype=float)

    mdp=""
    mdp += f"numStates {1000}\n" #+1 for wicket,state 1 :wicket
    mdp += f"numActions {8}\n"
    
    #print(prob)
    
    actions_A=[0,1,2,4,6]
    outcomes_A=[0,1,2,3,4,6]
    outcomes_B=[0,1]
    mx_bb=int(states[0][0]/100)
    mx_rr=states[0][0]%100
    #print(mx_rr)
    mdp += f"end 1"
    for rr in range(1,mx_rr+1):
        mdp += f" {get_str_states(rr,00,1)} {get_str_states(rr,00,2)}"
    for bb in range(1,mx_bb+1):
        mdp += f" {get_str_states(00,bb,1)} {get_str_states(00,bb,2)}"
    
    mdp += f"{get_str_states(00,00,1)} {get_str_states(00,00,2)} \n"   
    #mdp += "end " + " ".join(end) + "\n"

    for rr in range(1,mx_rr+1):
        for bb in range(1,mx_bb+1):
            for j in actions_A :
                prob[j][0]
                #-1
                mdp+=f"transition {get_str_states(rr,bb,1 )} {j} {1} 0.0 {prob[j][0]}\n"
                l=0
                for k in outcomes_A :
                    l+=1;
                    if (rr<=k):
                        mdp+=f"transition  {get_str_states(rr,bb,1 )} {j} {get_str_states(max(rr-k,0),bb-1,1 )} 1.0 {prob[j][l]}\n"
                    elif (bb==1):
                        mdp+=f"transition {get_str_states(rr,bb,1 )} {j} {get_str_states(max(rr-k,0 ),bb-1,1)} 0.0 {prob[j][l]}\n"
                    elif(((k==0) and ((bb-1)%6)!=0) or ((k==1) and ((bb-1)%6)==0) or ((k==2) and ((bb-1)%6)!=0) or ((k==3) and ((bb-1)%6)==0) or ((k==4) and ((bb-1)%6)!=0) or ((k==6) and ((bb-1)%6)!=0)):
                        mdp+=f"transition {get_str_states(rr,bb,1 )} {j} {get_str_states(max(rr-k,0 ),bb-1,1)} 0.0 {prob[j][l]}\n"
                    else :
                        mdp+=f"transition {get_str_states(rr,bb,1 )} {j} {get_str_states(max(rr-k,0 ),bb-1,2)} 0.0 {prob[j][l]}\n"
        
            
                #-1
            mdp+=f"transition {get_str_states(rr,bb,2)} {7} {1} 0.0 {q}\n"
                
            for k in outcomes_B :
                if (rr<=k):
                    mdp+=f"transition  {get_str_states(rr,bb,2 )} {7} {get_str_states(max(rr-k,0),bb-1,1 )} 1.0 {(1-q)/2}\n"
                elif (bb==1):
                    mdp+=f"transition {get_str_states(rr,bb,2 )} {7} {get_str_states(max(rr-k,0),bb-1,1 )} 0.0 {(1-q)/2}\n"
                elif(((k==0) and ((bb-1)%6)!=0) or ((k==1) and ((bb-1)%6)==0) or ((k==2) and ((bb-1)%6)!=0) or ((k==3) and ((bb-1)%6)==0) or ((k==4) and ((bb-1)%6)!=0) or ((k==6) and ((bb-1)%6)!=0)):
                    mdp+=f"transition {get_str_states(rr,bb,2 )} {7} {get_str_states(max(rr-k,0),bb-1,2 )} 0.0 {(1-q)/2}\n"
                else :
                    mdp+=f"transition {get_str_states(rr,bb,2 )} {7} {get_str_states(max(rr-k,0),bb-1,1 )} 0.0 {(1-q)/2}\n"

    mdp += "mdptype episodic\n"
    mdp += "discount  1"
    print(mdp)


if __name__ == "__main__":
    parser.add_argument("--states", type=str)
    parser.add_argument("--parameters", type=str)
    parser.add_argument("--q", type=float)
    args = parser.parse_args()
    encode(args.states,args.parameters,args.q)

    #python3 encoder.py --states /host/Assignment2/code/data/cricket/cricket_state_list.txt --parameters /host/Assignment2/code/data/cricket/sample-p1.txt  --q 0.45