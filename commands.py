import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime   # For getting time and date info


def run_and_log(command):
    '''
    This function is intended to simplify code writing as it compresses the execution, logging, and decoding of
    all console outputs from given operating system commands into one line, now one function.
    :param command: the input command
    :return: Returns the log
    '''
    result = subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read().decode("utf-8").replace("\r", "")
    return result


def release_and_renew_ip(os):
    '''
    Release and renews DHCP IP, also resets windows sockets. If this is NOT windows, it passes plain text to the log.
    :param os: operating system of the machine currently running the program
    :return: Returns console logs of the commands to be exported into the final log file
    '''
    if os != 'windows':
        release_result = "\nRelease command passed: Unix requires sudo"
        renew_result = "\nRenew command passed: Unix requires sudo"
        netsh_result = "\nNetsh command passed: Unix requires sudo"
    else:
        release_command = ['ipconfig', '/release']  # release current IP
        renew_command = ['ipconfig', '/renew']  # renew DHCP IP lease
        netsh_command = ['netsh', 'winsock', 'reset']   # resets the windows network socket system

        release_result = run_and_log(release_command)  # executes and logs the command to the defined variable
        time.sleep(5)   # wait 5 seconds
        renew_result = run_and_log(renew_command)  # executes and logs the command to the defined variable
        time.sleep(5)   # wait 5 seconds
        netsh_result = run_and_log(netsh_command)  # executes and logs the command to the defined variable
    return release_result, renew_result, netsh_result


def flush_and_register_dns(os):
    '''
    Flushes and registers fresh DNS cache. If this is NOT windows, it passes plain text to the log.
    :param os: operating system of the machine currently running the program
    :return: Returns console logs of the commands to be exported into the final log file
    '''
    if os != 'windows':
        flush_result = "\nDNS flush command passed as system is Unix based and requires sudo"
        register_result = "\nDNS registration command passed as system is Unix based and requires sudo"
    else:
        flush_command = ['ipconfig', '/flushdns']  # flushes current DNS
        register_command = ['ipconfig', '/registerdns']  # requests windows to reapply DNS to all adapters

        flush_result = run_and_log(flush_command)  # executes and logs the command to the defined variable
        time.sleep(5)  # wait 5 seconds
        register_result = run_and_log(register_command)  # executes and logs the command to the defined variable
    return flush_result, register_result


def ping(host, os, testType):
    '''
    Ping test to the defined host for 100 pings at max MTU size.
    :param host: ping test destination
    :param os: operating system of the machine currently running the program
    :param testType: defines weather the test is short or long (10 or 1000 pings)
    :return: string of console logs (decoded from byte to string, removed carriage returns)
    '''
    if os == 'windows':
        param_count_flag, param_MTU = '-n', '-l'
    else:
        param_count_flag, param_MTU = '-c', '-s'
    if testType == 'comprehensive':
        param_count_number = "1000"
    else:
        param_count_number = "10"
    command = ['ping', param_count_flag, param_count_number, param_MTU, '1472', host]   # Command itself
    ping_result = run_and_log(command)  # executes and logs the command to the defined variable
    return ping_result


def traceroute(host, os):
    '''
    Runs a traceroute to the defined host with max hops of 20 to ensure it does not
    infinitely run and continuously timeout as that can happen if not capped.
    :param host: traceroute destination
    :param os: operating system of the machine currently running the program
    :return: string of console logs (decoded from byte to string, removed carriage returns)
    '''
    if os == 'windows':
        param_command, param_hops = 'tracert', '-h'
    else:
        param_command, param_hops = 'traceroute', '-m'
    command = [param_command, param_hops, "20", host]   # Command itself
    trace_result = run_and_log(command)  # executes and logs the command to the defined variable
    return trace_result


def ipconfig(os):
    '''
    Fetches the IP configuration and hardware ID info for network card MACs, IPs, DNS, Subnets, etc.
    :param os: operating system of the machine currently running the program
    :return: string of ipconfig info console log (decodes from byte to string, removed carriage returns)
    '''
    if os == 'windows':
        param_command, param_flag = 'ipconfig', '/all'
    else:
        param_command, param_flag = 'ifconfig', '-a'
    command = [param_command, param_flag]   # Command itself
    network_config = run_and_log(command)  # executes and logs the command to the defined variable
    return network_config


# def speed_test(server):
#     # This function does not exist as the speed_test api for python is garbage and produces lies
#     return result_string



def Diagnostic():
    # set hostname, gather OS info, set time and date start
    hostname = "google.ca"
    print("Welcome to the Diagnostic command line")
    user_testType = input("If you would like to run a comprehensive ping test, please type 'yes' and hit enter"
                     "\notherwise, type 'no'.")
    if user_testType == 'yes':
        testType = "comprehensive"
    else:
        testType = "basic"

    operating_system = platform.system().lower()
    date_and_time = datetime.now().strftime("%d-%b-%Y_%I.%M.%p")

    # collect data
    ipconfig_output = ipconfig(operating_system)
    ping_output = ping(hostname, operating_system, testType)
    traceroute_output = traceroute(hostname, operating_system)

    # write data to single output variable and then write to file
    output = date_and_time + "\n\n" + ipconfig_output + "\n" + ping_output + "\n" + traceroute_output
    with open('Uniserve_Diagnostic_' + date_and_time + '.log', 'w') as outfile:
        outfile.write(output)


Diagnostic()