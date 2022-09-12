import os 
from datetime import datetime
from git import Repo
import Color 
import Symbol 

def print_grave() -> str:
    return print(f"\n{Symbol.grave}") 

def print_tilde() -> str:
    return print(f"\n{Symbol.tilde}") 

def print_exmak() -> str:
    return print(f"\n{Symbol.exmak}") 

def print_atsym() -> str:
    return print(f"\n{Symbol.atsym}") 

def print_pound() -> str:
    return print(f"\n{Symbol.pound}") 

def print_dollr() -> str:
    return print(f"\n{Symbol.dollr}") 

def print_pcent() -> str:
    return print(f"\n{Symbol.pcent}") 

def print_carat() -> str:
    return print(f"\n{Symbol.carat}") 

def print_amper() -> str:
    return print(f"\n{Symbol.amper}") 

def print_aster() -> str:
    return print(f"\n{Symbol.aster}") 

def print_oprnt() -> str:
    return print(f"\n{Symbol.oprnt}") 

def print_cprnt() -> str:
    return print(f"\n{Symbol.cprnt}") 

def print_hyphn() -> str:
    return print(f"\n{Symbol.hyphn}") 

def print_under() -> str:
    return print(f"\n{Symbol.under}") 

def print_equal() -> str:
    return print(f"\n{Symbol.equal}") 

def print_pluss() -> str:
    return print(f"\n{Symbol.pluss}") 

def print_osqbr() -> str:
    return print(f"\n{Symbol.osqbr}") 

def print_csqbr() -> str:
    return print(f"\n{Symbol.csqbr}") 

def print_bslsh() -> str:
    return print(f"\n{Symbol.bslsh}") 

def print_fslsh() -> str:
    return print(f"\n{Symbol.fslsh}") 

def print_vpipe() -> str:
    return print(f"\n{Symbol.vpipe}") 

def print_scoln() -> str:
    return print(f"\n{Symbol.scoln}") 

def print_colon() -> str:
    return print(f"\n{Symbol.colon}") 

def print_squte() -> str:
    return print(f"\n{Symbol.squte}") 

def print_dqute() -> str:
    return print(f"\n{Symbol.dqute}") 

def print_comma() -> str:
    return print(f"\n{Symbol.comma}") 

def print_perid() -> str:
    return print(f"\n{Symbol.perid}") 

def print_lessb() -> str:
    return print(f"\n{Symbol.lessb}") 

def print_moreb() -> str:
    return print(f"\n{Symbol.moreb}") 

def print_qustm() -> str:
    return print(f"\n{Symbol.qustm}") 

def print_console() -> str:   
    size = os.get_terminal_size()  

    user_name = os.getlogin()
    current_path = os.getcwd()
    current_path = "~\\" + "\\".join(current_path.split("\\")[-3:])
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    repo_path = os.getcwd()
    root_path = repo_path.split("\\")[0] + "\\"
    found_git = False 

    while found_git == False:
        if repo_path == root_path:
            break
        
        try: 
            repo = Repo(repo_path)
        except:
            repo_path = os.path.dirname(repo_path)
            continue

        found_git = True
        branch = repo.active_branch
    
    user_name = f"{Color.Yellow}{user_name}{Color.Reset}"
    current_path = f"{Color.Cyan}{current_path}{Color.Reset}"
    current_date = f"{Color.White}{current_date}{Color.Reset}"
    branch_name = f"{Color.Red}\ue0a0 {branch.name}{Color.Reset}"

    print(f"\n{size.columns * '#'}")    
    print(f"{user_name} in {current_path} | {current_date} on {branch_name}")
