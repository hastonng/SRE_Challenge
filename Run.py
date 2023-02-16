import requests
import json
import sys
import threading


SERVICES = [
    'PermissionsService',
    'AuthService',
    'MLService',
    'StorageService',
    'TimeService',
    'GeoService',
    'TicketService',
    'RoleService',
    'IdService',
    'UserService'
]

f_stop = threading.Event()

class CPX:

    def __init__(self):

        self.session = requests.session()
        self.service_list = []
        self.unhealthy_list = []
        self.risky_list = []
        self.healthy_list = []
        self.optimise_range = [{'min_range': 0, 'max_range': 65, 'status': 'Healthy'},
                               {'min_range': 65, 'max_range': 80, 'status': 'Risky'},
                               {'min_range': 80, 'max_range': 999, 'status': 'Unhealthy'}]

    def get_services(self, f_stop):
        """
        This function will get services
        """
        # Clear list
        self.service_list = []
        self.unhealthy_list = []
        self.risky_list = []
        self.healthy_list = []

        # URL as localhost
        url = "http://localhost:8080/servers"
        resp = self.session.get(url=url, verify=False)
        resp_dict = json.loads(resp.text)

        for ip in resp_dict:
            # For every IP in the server, get their data through requests
            url2 = "http://localhost:8080/" + ip
            resp2 = self.session.get(url=url2, verify=False)
            resp_dict2 = json.loads(resp2.text)
            resp_dict2['IP'] = ip

            # Append into a list for all IPs
            self.service_list.append(resp_dict2)

        for service in self.service_list:

            # if service['service'] == 'PermissionsService':

            self.get_overall_status(service=service)

            if service['cpu_integer'] in range(80, 999) and service['memory_integer'] in range(80, 999):
                service['IP'] = " [!] " + service['IP']

                self.unhealthy_list.append(service)

            if service['cpu_integer'] in range(65, 80) or service['memory_integer'] in range(65, 80):

                self.risky_list.append(service)

            if service['cpu_integer'] in range(0, 65) and service['memory_integer'] in range(0, 65):

                self.healthy_list.append(service)

        if not f_stop.is_set():
            # call get_services function again in 10 seconds
            threading.Timer(10, self.get_services, [f_stop]).start()



    def get_overall_status(self, service):

        """
        This function will calculate the required info for all IP services.

        :param service: Object
        :return: None
        """

        cpu_elements = service['cpu'].split('%')
        memory_elements = service['memory'].split('%')
        cpu_per = int(cpu_elements[0])
        mem_per = int(memory_elements[0])

        # Append integer values
        service['cpu_integer'] = cpu_per
        service['memory_integer'] = mem_per

        # Calculate the mean of both memory and cpu
        overall_ave = round((cpu_per + mem_per) / 2)

        # Check if overall status usage.
        for items in self.optimise_range:
            if overall_ave in range(items['min_range'], items['max_range']):
                service['overall_status'] = items['status']

            if cpu_per in range(items['min_range'], items['max_range']):
                service['cpu'] = service['cpu'] + " - " + items['status']

            if mem_per in range(items['min_range'], items['max_range']):
                service['memory'] = service['memory'] + " - " + items['status']



    def get_details_by_type(self, input_type):

        total_cpu_usage = 0
        total_mem_usage = 0
        count = 0

        print('\n')
        print("\tIP \t\t Service \t\t Overall Status \t\t CPU \t\t Memory")
        print("=======================================================================================================================")

        for service in self.service_list:

            if service['service'] == input_type:

                total_cpu_usage += int(service['cpu_integer'])
                total_mem_usage += int(service['memory_integer'])
                count += 1

                print(f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

        print("=======================================================================================================================")

        average_mem = total_mem_usage / count
        average_cpu = total_cpu_usage / count

        print('\n')
        print(f"Type:  \t {input_type:>12}")
        print('\n')
        print(f"Total Number of IPs:  \t\t{str(count):>5}")
        print("Total average CPU usage: \t%.2f" % average_cpu + "%")
        print("Total average memory usage: \t%.2f" % average_mem + "%")
        print('\n')

        print("=======================================================================================================================")

    def print_overall_services(self):

        print('\n')
        print("\tIP \t\t Service \t\t Overall Status \t\t CPU \t\t Memory")
        print(
            "=================================================================================================================================")

        for service in self.service_list:
            print(
                f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

        print(
            "=================================================================================================================================")
        print('\n')
        print("Press [1] to view according to CPU")
        print("Press [2] to view according to Memory")
        print("Press [3] to view according to highest usage")
        print("Press [4] to return")
        print("\n")

        while True:

            flag = int(input())

            if flag == 1:

                newlist = sorted(self.service_list, key=lambda d: d['cpu_integer'], reverse=True)

                self.service_list = newlist

                print('\n')
                print("\tIP \t\t Service \t\t Overall Status \t\t CPU \t\t Memory")
                print(
                    "=================================================================================================================================")

                for service in self.service_list:
                    print(
                        f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

                print(
                    "=================================================================================================================================")
                print('\n')
                print("Press [1] to view according to CPU")
                print("Press [2] to view according to Memory")
                print("Press [3] to view according to highest usage")
                print("Press [4] to return")
                print("\n")

            elif flag == 2:

                newlist = sorted(self.service_list, key=lambda d: d['memory_integer'], reverse=True)

                self.service_list = newlist

                print('\n')
                print("\tIP \t\t Service \t\t Overall Status \t\t CPU \t\t Memory")
                print(
                    "=================================================================================================================================")

                for service in self.service_list:
                    print(
                        f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

                print(
                    "=================================================================================================================================")
                print('\n')
                print("Press [1] to view according to CPU")
                print("Press [2] to view according to Memory")
                print("Press [3] to view according to highest usage")
                print("Press [4] to return")
                print("\n")

            elif flag == 3:

                newlist = sorted(self.unhealthy_list, key=lambda d: (d['memory_integer'], d['cpu_integer']), reverse=True)

                self.unhealthy_list = newlist

                print('\n')
                print("\tIP \t\t Service \t\t Overall Status \t\t CPU \t\t Memory")
                print(
                    "=================================================================================================================================")
                print("\tUNHEALTHY")
                print(
                    "=================================================================================================================================")
                for service in self.unhealthy_list:
                    print(
                        f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

                print(
                    "=================================================================================================================================")

                newlist2 = sorted(self.risky_list, key=lambda d: (d['memory_integer'], d['cpu_integer']),
                                 reverse=True)

                self.risky_list = newlist2
                print("\tRISKY")
                print(
                    "=================================================================================================================================")

                for service in self.risky_list:
                    print(
                        f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

                print(
                    "=================================================================================================================================")

                newlist3 = sorted(self.healthy_list, key=lambda d: (d['memory_integer'], d['cpu_integer']),
                                  reverse=True)

                self.healthy_list = newlist3
                print("\tHEALTHY")
                print(
                    "=================================================================================================================================")

                for service in self.healthy_list:
                    print(
                        f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

                print(
                    "=================================================================================================================================")
                print('\n')
                print("Press [1] to view according to CPU")
                print("Press [2] to view according to Memory")
                print("Press [3] to view according to highest usage")
                print("Press [4] to return")
                print("\n")

            elif flag == 4:
                print('\n')
                print("Return to main \t :)")
                break
            else:
                print("Invalid command...")
                print('\n')
                print('\n')
                print("\tIP \t\t Service \t\t Overall Status \t\t CPU \t\t Memory")
                print(
                    "=================================================================================================================================")

                for service in self.service_list:
                    print(
                        f"{service['IP']:>15} \t {service['service']:>15} \t {service['overall_status']:>15} \t {service['cpu']:>15} \t {service['memory']:>15}")

                print(
                    "=================================================================================================================================")
                print('\n')
                print("Press [1] to view according to CPU")
                print("Press [2] to view according to Memory")
                print("Press [3] to view according to highest usage")
                print("Press [4] to return")
                print("\n")

def menu(cpx):

    print('\n')
    print("Select options by entering the number accordingly. Eg: 1")
    print('\n')
    print("Press [1] to view all service details")
    print("Press [2] to view service by type")
    print("Press [3] to Exit")

    item = int(input())

    if item == 1:

        cpx.print_overall_services()

    elif item == 2:

        print('\n')
        print("\t| Select type of services: ")
        print('\t| ')
        print('\t| ==================================')
        print('\t| ')
        for index in range(0, len(SERVICES)):
            print("\t| [" + str(index + 1) + "] " + SERVICES[index])

        index = int(input()) - 1

        if index > 9:
            print('\n')
            print('Invalid selection')
            print('\n')
        else:
            cpx.get_details_by_type(input_type=SERVICES[index])

    elif item == 3:
        f_stop.set()
        print('\n')
        print('Stopping system threads...')
        sys.exit(0)


if __name__ == '__main__':

    try:
        # Initialise CPX class
        cpx = CPX()

        while True:

            # Get all IP available services
            cpx.get_services(f_stop=f_stop)

            menu(cpx=cpx)
    except ValueError:

        print("Please do not enter empty line.")
        f_stop.set()

    except KeyError:

        print("Something has gone wrong...")
        print("Please try again.")
        f_stop.set()


