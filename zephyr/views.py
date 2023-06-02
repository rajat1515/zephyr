from django.shortcuts import render
from .zephyr_api import Zephyr
import re

def upload_xml(request):
    if request.method == 'POST':
        return_response = ''


        # # create nested folders
        folder_names = {
            'main_folder':  request.POST.get('main-folder-name', 'PEG_FY_24').strip() ,
            'sprint_folder': request.POST.get('sprint-name', 'Test').strip(),
            'automation_folder': request.POST.get('automated-run', 'PEG_Automated Run').strip(),
            'week_folder_name' : request.POST.get('sub_folder').strip(),
            'release_version' : request.POST.get('release_version').strip()

        }
        if not folder_names['release_version'].startswith('A360.'):
            return render(request, 'index.html', {'response':'Incorrect Release version Format'})

        z = Zephyr(request.POST.get('bearer_token').strip(), request.POST.get('project_key').strip())

        folder_present = {}
        parent_id = None

        for folder_key, folder_name in folder_names.items():
            try:
                folder_present[folder_key] = z.get_folder(folder_name, parent_id)
                if not folder_present[folder_key]:
                    folder_present[folder_key] = z.create_test_cycle_folder(folder_name, parent_id).json()
                parent_id = folder_present[folder_key]['id']
            except:
            
                return render(request, 'index.html', {'response':'Invalid Zephyr Token'})


        #   post JUnit test results
        for file in request.FILES.getlist('files'):
            file_name = file.name
            file_data = file.read()
            s = re.match(r'[a-zA-Z_\s]+',file_name)
            if s:
                post_results_resp = z.post_junit_results(f'{s.group().strip()}.xml', file_data)
                new_cycle =  post_results_resp.json()['testCycle']
                # print(new_cycle)
                # print(post_results_resp.status_code)

                if post_results_resp.status_code in [201, 200]:
                    # print(f"Results posted to FIQ's Zephyr Test Cycles")
                    return_response +=  f"{file_name}  posted to FIQ's Zephyr with KEY : {new_cycle['key']}. \n "
                else:
                    # print(f'Failed: {post_results_resp.text}')
                    return_response +=  f"{file_name} failed to post. \n "
                    continue

                
                # print(f"Created Cycle {new_cycle['key']} - ID: {str(new_cycle['id'])}")

                #   update test Cycle
                update_resp = z.update_cycle(
                    new_cycle['id'], new_cycle['key'], s.group().strip(), parent_id, folder_names['release_version']
                )
                if update_resp.status_code == 200:
                    # print(f"Updated new test cycle's Name and moved it to the target Folder")
                    return_response +=  f"Updated new test cycle's Name and moved it to the target Folder. \n\n " 

                else:
                    # print(f'Failed: {update_resp.text}')
                    return_response +=  f"{file_name} f'Failed: {update_resp.text} \n "

            else:
                return_response +=  f"{file_name} not matched with given criteria. \n "
        return render(request, 'index.html', {'response':return_response})

    return render(request, 'index.html')