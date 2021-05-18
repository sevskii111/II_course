import Eparser

# Функция возвращает строку с правилом в удобном формате: ЕСЛИ условие, ТО действие


def rule_repr(rule):
    LHS = []
    for attr, values in rule['LHS'].items():
        LHS.append(attr + " = " + "|".join(values))
    (RHSkey, RHSvalue) = list(rule['RHS'].items())[0]
    return "IF " + " & ".join(LHS) + " THEN " + RHSkey + " = " + RHSvalue

# Функция печатает рабочую память


def printRM():
    print("Memory:")
    for r, v in RM.items():
        print(r, " = ", v)

# Func returns a list of rules, pravaya ch kotorih = znach parametra


def getConflictRules(rules, goal):
    ruleset = []
    for rule in rules:
        attribute = list(rule['RHS'].keys())[0]
        if attribute == goal:
            ruleset.append(rule)
    return ruleset
# The function checks if there is at least one rule, the right side of which is the goal value.


def conflictRuleExists(rules, goal):
    for rule in rules:
        attribute = list(rule['RHS'].keys())[0]
        if attribute == goal:
            return True
    return False

# The function checks if this rule works.


def ruleWorks(rule, RM):
    conditions = rule['LHS']

    for param in conditions:
        if param in RM:
            if RM[param] not in conditions[param]:
                return False
        else:
            return False
    return True

# The function for the user to enter the default parameter in the working memory


def parameterInput(param, RM):
    value = input("Enter parameter value '" + param +
                  "' " + str(parameters[param+"*"]) + ": ")
    while(value not in parameters[param+"*"]):
        value = input()
    RM[param] = value

# Функция печатает атрибуты / параметры, их значения и все правила, содержащиеся в БЗ


def printKnowledgeBase(parameters, rules):
    print('-'*105)
    print('|' + '\t'*6 + 'Knowledge base' + '\t'*6 + '|')
    print('-'*105 + '\n')

    print("Attributes:")
    for attr, value in parameters.items():
        print(attr + " = " + " | ".join(value))

    print("\nRules:")
    for i, rule in enumerate(rules):
        print(str(i+1) + ") " + rule_repr(rule))

    print('-'*105 + '\n')


# Получить атрибуты и правила из базы знаний
parameters, rules = Eparser.parse('./Virus.txt')


# Print KB
printKnowledgeBase(parameters, rules)

# Working memory, stack with targets and a list of already verified attributes
RM = {}
goals = []
checked_goals = []

# Asks user to enter target hypothesis
goal = input('Please, enter "Virus": ')
goals.append(goal)

# Main loop
while(True):

    # # If stack is empty, quit
    if len(goals) == 0:
        break

    # Vspomog variab
    new_goal = False
    new_parameter = False
    # Save current target
    goal = goals[-1]
    # Create a set of conflicting rules and keep them count
    conflictRules = getConflictRules(rules, goal)
    remainingRules = len(conflictRules)
    # If no matching rule is found, stop the loop and notify the user.
    if remainingRules == 0:
        print('The knowledge base does not contain information about this virus.')
        break
    # Prints a set of rules and working memory.
    print('Rules: ')
    for cr in conflictRules:
        print(rule_repr(cr))
    printRM()
   # The cycle goes through a set of conflicting rules.
    # If the rule works:
    # 1) delete the current target from above
    # 2) keeps its right side in working memory
    # 3) set the variable new_goal to True and exit the loop
    for cr in conflictRules:
        if ruleWorks(cr, RM):
            (RHSkey, RHSvalue) = list(cr['RHS'].items())[0]
            RM[RHSkey] = RHSvalue
            curr_goal = goals.pop()
            print("Goal: " + curr_goal + " = " + RHSvalue)
            new_goal = True
            break
# If the target is updated
    if new_goal:
        continue
    # for each rule in the conflict rule set
    for cr in conflictRules:

        if new_goal:
            break
        # уменьшить количество непроверенных правил
        remainingRules -= 1
        conditions = cr['LHS']
        # for each parameter of checked rules
        for param in conditions:
           # if the parameter has already been checked and it was not possible to execute it,
            # skip rule (do not check other parameters)
            if param in checked_goals:
                break
            # if current parameter is in working memory
            if param in RM:
               # parameter value does not match the value in working memory
                if RM[param] not in conditions[param]:
                    break
            else:  # parameter is not in memory
                # if one of the rules fulfills the current parameter, set it as a target
                if conflictRuleExists(rules, param):
                    goals.append(param)
                    new_goal = True
                    break
                elif param + "*" in parameters:
                    # None of the rules executes the parameter
                    # if possible (the parameter name ends with '*'),
                    # asks user to enter parameter value
                    parameterInput(param, RM)
                    new_parameter = True
                    break
                else:
                   # parameter cannot be obtained from any rule
                    # user cannot login
                    checked_goals.append(param)
        if new_parameter:
            break

        # If a new target has not been established and all the rules have been verified, delete the target from above.
          # and save it to the list of goals that can not be achieved
        if remainingRules == 0 and not new_goal:
            curr_goal = goals.pop()
            checked_goals.append(curr_goal)
           # print ('The knowledge base does not contain information about this virus: ' + curr_goal)
            print('The knowledge base does not contain information about this virus: ')
    print('-'*100)
