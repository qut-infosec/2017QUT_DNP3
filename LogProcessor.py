import datetime
import re
from sets import Set
import string
import subprocess
find_cmd = 'find . -iname "*.log" -mindepth 5 -maxdepth 5'

attack_classes = {

    "injection": [
        "injection_replay",
        "injection_replay_updaterAck",
        "injection_FreezeObj",
        "injection_ColdRestart",
        "injection_WarmRestart",
        "injection_push",
    ],
    "masquerading": [
        "master_masquerading",
        "master_hijacking_masquerading",
        "slave_masquerading",
        "slave_masquerading_flooding",
        "slave_masquerading_ObjectSpoofBinary",
        "slave_masquerading_ObjectSpoofCounter",
        "slave_masquerading_ObjectSpoofBinaryFuzz",
        "slave_masquerading_ObjectSpoofCounterFuzz"
    ],
    "flooding": [
        "master_flooding",
        "slave_masquerading_flooding",
        "master_replay_flooding",
        "master_hijacking_replay_flooding",
        "master_flooding_freeze",
        "master_flooding_time",
    ],
    "replay": [
        "master_replay",
        "master_replay_flooding",
        "master_hijacking_replay",
        "injection_replay",
        "injection_replay_updaterAck",
    ],

    "MITM": [
        "MITM_forwarding",
        "MITM_hijack_injection",
        "MITM_modification_ImmedFreezeNR",
        "MITM_modification_BinaryStatus",
        "MITM_modification_CounterStatus",
        "MITM_modification_BinaryInputPointDelete",
        "MITM_modification_BinaryInputDataDelete",
        "MITM_modification_BinaryInputPointInsert",
        "MITM_modification_CountBinaryInputPointInsert"
    ],
    "attacks": [
        "injection_replay",
        "injection_replay_updaterAck",
        "injection_FreezeObj",
        "injection_ColdRestart",
        "injection_WarmRestart",
        "injection_push",
        "master_masquerading",
        "master_hijacking_masquerading",
        "slave_masquerading",
        "slave_masquerading_flooding",
        "slave_masquerading_ObjectSpoofBinary",
        "slave_masquerading_ObjectSpoofCounter",
        "slave_masquerading_ObjectSpoofBinaryFuzz",
        "slave_masquerading_ObjectSpoofCounterFuzz",
        "master_flooding",
        "master_replay_flooding",
        "master_hijacking_replay_flooding",
        "master_flooding_freeze",
        "master_flooding_time",
        "master_replay",
        "master_hijacking_replay",
        "MITM_forwarding",
        "MITM_hijack_injection",
        "MITM_modification_ImmedFreezeNR",
        "MITM_modification_BinaryStatus",
        "MITM_modification_CounterStatus",
        "MITM_modification_BinaryInputPointDelete",
        "MITM_modification_BinaryInputDataDelete",
        "MITM_modification_BinaryInputPointInsert",
        "MITM_modification_CountBinaryInputPointInsert"
    ]
}


attacklogs = [
"./Attacks/attacks/testing/frequent/Attack_script_log.log",
"./Attacks/attacks/testing/infrequent/Attack_script_log.log",
"./Attacks/attacks/training/frequent/Attack_script_log.log",
"./Attacks/attacks/training/infrequent/Attack_script_log.log",
"./Control/control/testing/frequent/Attack_script_log.log",
"./Control/control/testing/infrequent/Attack_script_log.log",
"./Control/control/training/frequent/Attack_script_log.log",
"./Control/control/training/infrequent/Attack_script_log.log",
"./Flooding/flooding/testing/frequent/Attack_script_log.log",
"./Flooding/flooding/testing/infrequent/Attack_script_log.log",
"./Flooding/flooding/training/frequent/Attack_script_log.log",
"./Flooding/flooding/training/infrequent/Attack_script_log.log",
"./Injection/injection/testing/frequent/Attack_script_log.log",
"./Injection/injection/testing/infrequent/Attack_script_log.log",
"./Injection/injection/training/frequent/Attack_script_log.log",
"./Injection/injection/training/infrequent/Attack_script_log.log",
"./Masqurading/masquerading/testing/frequent/Attack_script_log.log",
"./Masqurading/masquerading/testing/infrequent/Attack_script_log.log",
"./Masqurading/masquerading/training/frequent/Attack_script_log.log",
"./Masqurading/masquerading/training/infrequent/Attack_script_log.log",
"./MITM/MITM/testing/frequent/Attack_script_log.log",
"./MITM/MITM/testing/infrequent/Attack_script_log.log",
"./MITM/MITM/training/frequent/Attack_script_log.log",
"./MITM/MITM/training/infrequent/Attack_script_log.log",
"./Replay/replay/testing/frequent/Attack_script_log.log",
"./Replay/replay/testing/infrequent/Attack_script_log.log",
"./Replay/replay/training/frequent/Attack_script_log.log",
"./Replay/replay/training/infrequent/Attack_script_log.log",
]

labels = {
    'nmap': 0.1,
    'reconnaissance': 0.2,
    'injection_replay': 1.1,
    'injection_replay_updaterAck': 1.2,
    'injection_FreezeObj': 1.3,
    'injection_ColdRestart': 1.4,
    'injection_WarmRestart': 1.5,
    'injection_push': 1.6,
    'master_masquerading': 2.1,
    'master_hijacking_masquerading': 2.2,
    'slave_masquerading': 2.3,
    'slave_masquerading_ObjectSpoofBinary': 2.4,
    'slave_masquerading_ObjectSpoofCounter': 2.5,
    'slave_masquerading_ObjectSpoofBinaryFuzz': 2.6,
    'slave_masquerading_ObjectSpoofCounterFuzz': 2.7,
    'master_replay': 3.1,
    'master_hijacking_replay': 3.2,
    'master_replay_flooding': 4.2,
    'master_hijacking_replay_flooding': 4.3,
    'master_flooding': 4.1,
    'master_flooding_freeze': 4.4,
    'master_flooding_time': 4.5,
    'slave_masquerading_flooding': 4.6,
    'MITM_forwarding': 5.1,
    'MITM_hijack_injection': 5.2,
    'MITM_modification_ImmedFreezeNR': 5.3,
    'MITM_modification_BinaryStatus': 5.4,
    'MITM_modification_CounterStatus': 5.5,
    'MITM_modification_BinaryInputPointDelete': 5.6,
    'MITM_modification_BinaryInputDataDelete': 5.7,
    'MITM_modification_BinaryInputPointInsert': 5.8,
    'MITM_modification_CountBinaryInputPointInsert': 5.9,
}

labels_ = {
    0.1: "nmap",
    0.2: "reconnaissance",
    1.1: "injection_replay",
    1.2: "injection_replay_updaterAck",
    1.3: "injection_FreezeObj",
    1.4: "injection_ColdRestart",
    1.5: "injection_WarmRestart",
    1.6: "injection_push",
    2.1: "master_masquerading",
    2.2: "master_hijacking_masquerading",
    2.3: "slave_masquerading",
    2.4: "slave_masquerading_ObjectSpoofBinary",
    2.5: "slave_masquerading_ObjectSpoofCounter",
    2.6: "slave_masquerading_ObjectSpoofBinaryFuzz",
    2.7: "slave_masquerading_ObjectSpoofCounterFuzz",
    3.1: "master_replay",
    3.2: "master_hijacking_replay",
    4.1: "master_flooding",
    4.2: "master_replay_flooding",
    4.3: "master_hijacking_replay_flooding",
    4.4: "master_flooding_freeze",
    4.5: "master_flooding_time",
    4.6: "slave_masquerading_flooding",
    5.1: "MITM_forwarding",
    5.2: "MITM_hijack_injection",
    5.3: "MITM_modification_ImmedFreezeNR",
    5.4: "MITM_modification_BinaryStatus",
    5.5: "MITM_modification_CounterStatus",
    5.6: "MITM_modification_BinaryInputPointDelete",
    5.7: "MITM_modification_BinaryInputDataDelete",
    5.8: "MITM_modification_BinaryInputPointInsert",
    5.9: "MITM_modification_CountBinaryInputPointInsert",
}


class Log(object):
    def __init__(self):
        self.start = None
        self.finish = None
        self.attack = None

attacks_re = re.compile(r'\b(?:%s)\b' % "|".join(labels))
#log_file = 'Attack_script_log.log'
#lines = [line.rstrip('\n') for line in open(log_file)]
timestamp = re.compile('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[.]\d{6}')
utc_format = "%Y-%m-%d %H:%M:%S.%f"
start_time = '2016-10-13 13:10:29.420762'
start = datetime.datetime.strptime(str(start_time), utc_format)

def log_processor():
    logs = {

    }
    for log_file in attacklogs:
        logs[log_file] = []

        # log_file = 'Attack_script_log.log'
        lines = [line.rstrip('\n') for line in open(log_file)]
        log = Log()
        for l in lines:
            # print l
            m = re.search(timestamp, l)
            attack = attacks_re.search(l)
            time = m.group(0)
            dt = datetime.datetime.strptime(str(time), utc_format)
            if not log.start:
                log.start = dt
                log.attack = attack.group(0)

            elif (log.start is not None) and (log.attack == attack.group(0)):
                log.finish = dt
                logs[log_file].append(log)
                log = Log()
                # for l in logs:
                #    print str(labels[l.attack]) + "," + str((l.start - start).total_seconds()) + "," + str((l.finish - start).total_seconds()) #, l.attack

                # for l in sorted(labels_):
                #   print str(l)+":", "\""+labels_[l]+"\""


    for l in sorted(logs):
        name = l.split('/')
        attack_name = name[4] + " " + name[1] + " " + name[3]
        attack_name = string.capwords(attack_name)
        set = Set()
        for p in logs[l]:
            set.add(str(labels[p.attack]))
        print attack_name + ",", ' '.join(sorted(set)) + ",", len(logs[l])

if __name__ == '__main__':
    #log_processor()
    for attacks in attack_classes:
        print attacks
        for attack in attack_classes[attacks]:
            print labels[attack]