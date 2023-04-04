#!/usr/bin/env python3.9
#coding: utf-8

#Script to autodelete users from Dynamics CRM according to certain criterions
#By CORals 

import os
import PySimpleGUI as sg
from simple_dyn365 import Dynamics
import datetime

sg.theme('LightGrey1')

try:
    layoutAutodelete = [
        [sg.Text('')],
        [sg.Text('Delete outdated memberships (GDPR)', font='bold')],
        [sg.Text('')],
        [sg.Text('Choose log folder: ', size=(12,1))],
        [sg.In('', key='log_folder', size=(50,1)), sg.FolderBrowse()],
        [sg.Text('')],
        [sg.Button('Search and delete'), sg.Button('Avbryt')],
        [sg.Text('Log preview:')],
        [sg.Output(background_color='white', size=(56,5))],
        [sg.Text('')]]
    
    winAutodelete = sg.Window('GDPR Autodelete by CORals Analytics', default_element_size=(40, 1), grab_anywhere=False, location=(100,100)).Layout(layoutAutodelete)

    while True:
        evAutodelete,valAutodelete=winAutodelete.Read(timeout=100)
        
        if evAutodelete is None or evAutodelete=='Avbryt':
            winAutodelete.Close()
            del winAutodelete
            break
        

        #Popup for exceptions:
        def popup_break(event, message):
            while True:
                sg.Popup(message)
                event='False'
                break           

        if evAutodelete=='Search and delete' and valAutodelete['log_folder']=='':
            popup_break(evAutodelete, 'Please, choose log folder')
        
        elif evAutodelete=='Search and delete' and not valAutodelete['log_folder']=='':
            now='{date:%Y-%m-%d_%H-%M-%S}'.format( date=datetime.datetime.now() )
            now=f'{now}'
            filename='Autodelete_log_GDPR_' + now + '.txt'
            full_filename=os.path.join(valAutodelete['log_folder'], filename)
            deleted_contacts = []
            deleted_contacts.append(now + ':')
            deleted_nr = 0

            #Script to access contacts in Dynamics 365 CRM for CRUD - purpose: 

            """
            #Ref: https://github.com/adam-mah/simple-dyn365
            #Connect to database: (Creates dictionary??)
            dyn = Dynamics(client_id='', client_secret='', tenant_id='', crm_org='https://nokrifa.crm4.dynamics.com')
            #Get contacts metadata: 
            contacts=dyn.contacts.metadata()

            #Loop through all contacts:
            for contact in contacts: 
                if "Medlemskap avsluttet for mer enn 5 år siden" and "Ingen sakskommunikasjon siste 10 år":
                    contact_str=str(contact)
                    contact_name=dyn.contacts.get('First_name') + '_' + dyn.contacts.get('Last_name')
                    contact_str_full=contact_name + '_' + contact_str
                    deleted_contacts.append(contact_str_full)
                    dyn.contacts.delete(contact)
                    deleted_nr += 1
            
            """
            
            #List of deleted contacts, included total number:
            deleted_contacts.append('Totalt antall slettet i CRM: ' + str(deleted_nr))

            #Rapport i loggfil:
            with open(full_filename,'w') as logfile:
                for item in deleted_contacts:
                    logfile.write("%s\n" % item)
            
            #Rapport i logg i interface:
            print(now + ':')
            print('Search completed.')
            print('Number of condtacts deleted due to GDPR: ' + str(deleted_nr))
            print('Log location: ' + valAutodelete['log_folder'] + '.')
            print('Done')
            print('')


except:
    sg.Popup('Ooops! Something went wrong:(')

    