import pandas as pd
import numpy as np
import PySimpleGUI as sg

#KK, NIK : boleh kosong


# Add some color to the window
sg.theme('SandyBeach')

def draw_plot():
    plt.plot([0.1, 0.2, 0.5, 0.7])
    plt.show(block=False)

df_ind = pd.read_excel('Database\Data Individu.xlsx',
                       dtype={'ID' : 'str', #supaya ga ke convert balik ke int
                              'No' : 'str',
                              'KK' : 'str',
                              'Jorong' : 'str',
                              'NIK' : 'str',
                              'Nama' : 'str'})
df_ruta = pd.read_excel('Database\Data Rumah Tangga.xlsx',
                      dtype={'ID_2': 'str'}
                      )
layout_ind = [
    [sg.Text('ID Keluarga', size=(20,1)), sg.InputText(key='ID')],  
    [sg.Text('No', size=(20,1)), sg.InputText(key='No'),sg.Button('Cari Individu')],
    [sg.Text('Nomor KK', size=(20,1)), sg.InputText(key='KK')],
    [sg.Text('Jorong', size=(20,1)), sg.InputText(key='Jorong')],
    [sg.Text('Nama', size=(20,1)), sg.InputText(key='Nama')],
    [sg.Text('Status', size=(20,1)), sg.InputText(key='Status')],    
    [sg.Text('Jenis Kelamin', size=(20,1)), sg.InputText(key='Jenis_Kelamin')],
    [sg.Text('Tanggal Lahir (HH/BB/TT)', size=(20,1)), sg.Combo(list(range(1,32)),key='Hari'), sg.Combo(list(range(1,13)),key='Bulan'),sg.Combo(list(range(1920,2022)),key='Tahun')],
    [sg.Text('Agama', size=(20,1)), sg.InputText(key='Agama')],
    [sg.Text('Ijazah', size=(20,1)), sg.InputText(key='Ijazah')],
    [sg.Text('Pekerjaan', size=(20,1)), sg.InputText(key='Pekerjaan')],
    [sg.Text('NIK', size=(20,1)), sg.InputText(key='NIK')],
    [sg.Submit('Simpan Informasi Individu'), sg.Button('Kosongkan'), sg.Exit('Keluar')],
    [sg.Button('Rekap'), sg.Button('Export Data Individu'), sg.Button('Analisis')]
]

layout_ruta = [    
    [sg.Text('ID Keluarga', size=(20,1)), sg.InputText(key='ID_2')],
    [sg.Button('Cari Keluarga')],
    [sg.Text('Lahan Perumahan (m2)', size=(20,1)), sg.InputText(key='Lahan_Perumahan')],
    [sg.Text('Lahan Pertanian (Ha)', size=(20,1)), sg.InputText(key='Lahan_Pertanian')],
    [sg.Text('Lahan Perkebunan (Ha)', size=(20,1)), sg.InputText(key='Lahan_Perkebunan')],
    [sg.Text('Sapi', size=(20,1)), sg.InputText(key='Sapi')],
    [sg.Text('Kambing', size=(20,1)), sg.InputText(key='Kambing')],
    [sg.Text('Ayam Kampung', size=(20,1)), sg.InputText(key='Ayam_Kampung')],
    [sg.Text('Bebek', size=(20,1)), sg.InputText(key='Bebek')],
    [sg.Text('Itik', size=(20,1)), sg.InputText(key='Itik')],
    [sg.Text('Ayam Petelur', size=(20,1)), sg.InputText(key='Ayam_Petelur')], 
    [sg.Submit('Simpan Informasi Keluarga'), sg.Button('Kosongkan'), sg.Exit('Keluar')],
    [sg.Button('Export Data Ruta')]
]

                  

tabgrp = [[sg.TabGroup([[sg.Tab('Individu', layout_ind),
                         sg.Tab('Keluarga', layout_ruta)]],
                       tab_location='centertop')]]

window = sg.Window('Pendataan Nagari Sitiung: September 2021', tabgrp,
                   auto_size_text = True,
                   auto_size_buttons=True,
                   element_justification='center', font='Helvetica 15', finalize=True)


def clear_input():
    for key in values:
        window[key]('')
    return None


while True:
    event, values = window.read()

    #Kalo di close atau exit:
    if event == sg.WIN_CLOSED or event == 'Keluar':
        break

    #Kalo di clear
    if event == 'Kosongkan':
        clear_input()

    #Kalo di export
    if event == 'Export Data Individu':
        df_ind.to_excel('Data Individu.xlsx', index=False)
        sg.popup('Data Berhasil di Export')

    #Kalo di export
    if event == 'Export Data Ruta':
        df_ruta.to_excel('Data Rumah Tangga.xlsx', index=False)
        sg.popup('Data Berhasil di Export')

    #Kalo di rekap:
    if event == 'Rekap':
        rekap_ind = pd.read_excel('Database\Data Individu.xlsx',
                       dtype={'ID' : 'str',
                              'No' : 'str',
                              'KK' : 'str',
                              'Jorong' : 'str',
                              'NIK' : 'str',
                                      'Nama' : 'str'})
        
        jorong = {'kode' : ['001','002','003','004','005','006','007','008','009','010','011','012','013'],
                 'nama' : ['Sitiung','Koto Sitiung','Sitiung Tangah',
                           'Sitiung Agung', 'Pulai','Sungai Bai',
                           'Piruko Selatan','Piruko Tengah','Piruko Utara',
                           'Piruko Timur','Lawai','Padang Sidondang',
                           'Pisang Rebus']} 

        masterjor = pd.DataFrame.from_dict(jorong)

        df_rekap=pd.merge(rekap_ind,masterjor,how='left',left_on='Jorong',right_on='kode')
        tabel_plot = df_rekap[['ID','nama']].groupby('nama').agg('count').reset_index()
        tabel_plot = tabel_plot.values.tolist()
        layout_rekap = [[sg.Text("Rekapitulasi Entry")],
                  [sg.Table(values=tabel_plot,
                          headings=['Jorong','Jumlah'],
                          key='Tabel',                
                          display_row_numbers=False,
                          auto_size_columns=True,
                          num_rows=min(25, len(tabel_plot)))]
                  ]
        window_rekap = sg.Window("Rekapitulasi Entry", layout_rekap, modal=True)
        choice = None
        while True:
            event, values = window_rekap.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break            
        window_rekap.close()

    #Kalo di analisis:
    if event == 'Analisis':
        analisis_ind = pd.read_excel('Database\Data Individu.xlsx',
                       dtype={'ID' : 'str',
                              'No' : 'str',
                              'KK' : 'str',
                              'Jorong' : 'str',
                              'NIK' : 'str',
                                      'Nama' : 'str'})
        
        jorong = {'kode' : ['001','002','003','004','005','006','007','008','009','010','011','012','013'],
                 'nama' : ['Sitiung','Koto Sitiung','Sitiung Tangah',
                           'Sitiung Agung', 'Pulai','Sungai Bai',
                           'Piruko Selatan','Piruko Tengah','Piruko Utara',
                           'Piruko Timur','Lawai','Padang Sidondang',
                           'Pisang Rebus']} 

        masterjor = pd.DataFrame.from_dict(jorong)

        df_analisis=pd.merge(analisis_ind,masterjor,how='left',left_on='Jorong',right_on='kode')
        
        tabel_plot = df_analisis[['ID','nama']].groupby('nama').agg('count').reset_index()
        tabel_plot = tabel_plot.values.tolist()
        draw_plot() #tinggal list variabel mana yang mau divisual
            

    #Kalo di cari individu
    if event == 'Cari Individu':
        if (df_ind.loc[(df_ind['ID'] == values['ID']) & (df_ind['No']==values['No'])].index.tolist() != [] ) :
           #masih kepisah
            sg.popup('Individu ditemukan!')
            condition = (df_ind['ID'] == values['ID']) & (df_ind['No'] == values['No'])
            values = df_ind[condition]
            window['KK'].update(values['KK'].values[0])
            window['Jorong'].update(values['Jorong'].values[0])
            window['Nama'].update(values['Nama'].values[0])
            window['Status'].update(values['Status'].values[0])
            window['Jenis_Kelamin'].update(values['Jenis_Kelamin'].values[0])
            window['Hari'].update(values['Hari'].values[0])
            window['Bulan'].update(values['Bulan'].values[0])
            window['Tahun'].update(values['Tahun'].values[0])
            window['Agama'].update(values['Agama'].values[0])
            window['Ijazah'].update(values['Ijazah'].values[0])
            window['Pekerjaan'].update(values['Pekerjaan'].values[0])
            window['NIK'].update(values['NIK'].values[0])
        else:
            sg.popup('Individu belum ada di database!')
            
    #Kalo di cari keluarga
    if event == 'Cari Keluarga':
        if values['ID_2'] in list(df_ruta['ID_2']):
            sg.popup('ID ditemukan!')
            values = df_ruta[df_ruta['ID_2'] == values['ID_2']]
            window['Lahan_Perumahan'].update(values['Lahan_Perumahan'].values[0])
            window['Lahan_Pertanian'].update(values['Lahan_Pertanian'].values[0])
            window['Lahan_Perkebunan'].update(values['Lahan_Perkebunan'].values[0])
            window['Sapi'].update(values['Sapi'].values[0])
            window['Kambing'].update(values['Kambing'].values[0])
            window['Ayam_Kampung'].update(values['Ayam_Kampung'].values[0])
            window['Bebek'].update(values['Bebek'].values[0])
            window['Itik'].update(values['Itik'].values[0])
            window['Ayam_Petelur'].update(values['Ayam_Petelur'].values[0])           
        else:
            sg.popup('Keluarga belum ada di database!')
            
    #Kalo di Submit Individu
    if event == 'Simpan Informasi Individu':        
        #1. Cek Error Belom Lengkap
        error_Kosong = (values['ID']=='') or (values['No']=='') or (values['Jorong']=='') or (values['Nama']=='') or (values['Status']=='') or (values['Jenis_Kelamin']=='') or (values['Agama']=='') or (values['Ijazah']=='') or (values['Pekerjaan']=='') or (values['Hari']=='') or (values['Bulan']=='') or (values['Tahun']=='')      
        if error_Kosong: #if level 1
            sg.popup('Masih ada yang belum terisi!')
        else:
            #2. Cek Error Non Numerik, kecuali KK dan NIK bisa lewat karena bisa kosong
            try:                               
                int(values['ID'])
                int(values['No'])
                if (values['KK']!=''):
                    int(values['KK']) 
                int(values['Jorong'])
                values['Status'] = int(values['Status'])
                values['Jenis_Kelamin'] = int(values['Jenis_Kelamin'])
                values['Hari'] = int(values['Hari'])
                values['Bulan'] = int(values['Bulan'])
                values['Tahun'] = int(values['Tahun'])
                values['Agama'] = int(values['Agama'])
                values['Ijazah'] = int(values['Ijazah'])
                values['Pekerjaan'] = int(values['Pekerjaan'])
                if (values['NIK'] !=''):
                    int(values['NIK'])
                error_Non_numerik = False
            except ValueError:
                error_Non_numerik = True
            
            if error_Non_numerik: #If level 2: Cek numerik
                sg.popup('Pastikan kembali seluruh isian berupa angka, kecuali nama!')
                
            else:
                #3. Cek Range
                msg_element = [] #dummy list buat nampung error message
                msg='' #dummy value untuk simpen concatenate per element
                if (values['KK']!=''):
                    error_KK = len(values['KK'])!=16
                else:
                    error_KK = False
                error_ID = len(values['ID'])!= 4 
                error_No = int(values['No']) not in list(range(1,11))
                error_Jorong = (len(values['Jorong'])!= 3) or (int(values['Jorong']) not in list(range(1,14)))
                error_Nama = any(map(str.isdigit, values['Nama']))
                error_Status = values['Status'] not in list(range(1,5))
                error_JenisKelamin = values['Jenis_Kelamin'] not in [1,2]
                error_TanggalLahir = ((values['Hari'] >29) and (values['Bulan'] == 2)) or ((values['Hari'] >30) and (values['Bulan'] in [2,4,6,9,11]))
                error_Agama = values['Agama'] not in list(range(1,8))
                error_Ijazah = values['Ijazah'] not in list(range(1,9))
                error_Pekerjaan = values['Pekerjaan'] not in list(range(0,10))
                
                if (values['NIK'] !=''):
                    error_NIK = len(values['NIK'])!=16
                else:
                    error_NIK = False                       
                if (error_KK) or (error_ID) or (error_No) or (error_Jorong) or (error_Nama) or(error_Status) or (error_JenisKelamin) or (error_TanggalLahir) or (error_Agama) or (error_Ijazah) or (error_Pekerjaan) or (error_NIK): #If level 3 per variabel
                    if error_KK:
                        msg_element.append('Jumlah Digit KK tidak sama dengan 16!')
                    if error_ID:
                        msg_element.append('Jumlah Digit ID Keluarga tidak sama dengan 4!')
                    if error_No:
                        msg_element.append('Nomor ART di luar range!')
                    if error_Jorong:
                        msg_element.append('Jumlah Digit Jorong tidak sama dengan 3 atau bernilai di luar 010 hingga 013')
                    if error_Nama:
                        msg_element.append('Nama megandung angka!')
                    if error_Status:
                        msg_element.append('Kode Status di luar range!')
                    if error_JenisKelamin:
                        msg_element.append('Kode Jenis Kelamin di luar range!')
                    if error_TanggalLahir:
                        msg_element.append('Periksa Kembali Tanggal Lahir!')
                    if error_Agama:
                        msg_element.append('Kode Agama di luar range!')
                    if error_Ijazah:
                        msg_element.append('Kode Ijazah di luar range!')
                    if error_Pekerjaan:
                        msg_element.append('Kode Pekerjaan di luar range!')
                    if error_NIK:
                        msg_element.append('Jumlah Digit NIK tidak sama dengan 16!')                    
                    for i in msg_element:
                        msg += str(msg_element.index(i)+1) + '. ' + i + '\n'
                    sg.popup(msg)
                else:
                    values_ind = {x: values[x] for x in values.keys() if x in
                                  ['ID','No','KK','Jorong','Nama','Status','Hari',
                                   'Bulan','Tahun','Jenis_Kelamin','Agama',
                                   'Ijazah','Pekerjaan','NIK']}
                    if (df_ind[(df_ind['ID'] == values_ind['ID']) & (df_ind['No'] == values_ind['No'])].index.tolist() != []):
                        sg.set_options(auto_size_buttons=True)
                        layout_konfirm_ind = [[sg.Text('Ubah Informasi Individu?', size=(16, 1))],
                                              [sg.Button('Ya'),sg.Button('Tidak')]
                                              ]
                        window1 = sg.Window('Individu dengan ID keluarga dan No ART sudah ada di database!', layout_konfirm_ind, auto_size_text=True)
                        try:
                            event,values = window1.read()
                            if event == 'Ya':
                                window1.close()
                                condition = (df_ind['ID'] == values_ind['ID']) & (df_ind['No'] == values_ind['No']) #harus & ga bisa 'and'
                                df_ind[condition] = pd.DataFrame(values_ind, index = df_ind[condition].index.tolist())
                                df_ind.to_excel('Database\Data Individu.xlsx', index=False)
                                sg.popup('Data Individu Berhasil Diperbarui!')
                                clear_input()
                            if event =='Tidak':
                                window1.close()
                        except:
                            window1.close()
                    else:                        
                        df_ind = df_ind.append(values_ind, ignore_index=True)
                        df_ind.to_excel('Database\Data Individu.xlsx', index=False)
                        sg.popup('Data Individu Tersimpan')
                        clear_input()
   


    #Kalo di Submit Keluarga  
    if event == 'Simpan Informasi Keluarga':        
        #1. Cek Error Belom Lengkap
        error_Kosong = ((values['ID_2']=='') or
                        (values['Lahan_Perumahan']=='') or
                        (values['Lahan_Pertanian']=='') or
                        (values['Lahan_Perkebunan']=='') or
                        (values['Sapi']=='') or
                        (values['Kambing']=='') or
                        (values['Ayam_Kampung']=='') or
                        (values['Bebek']=='') or
                        (values['Itik']=='') or
                        (values['Ayam_Petelur']=='')
                        )
        if error_Kosong: #if level 1
            sg.popup('Masih ada yang belum terisi!')
        else:
            #2. Cek Error Non Numerik, kecuali KK dan NIK bisa lewat karena bisa kosong: selain ID sekalian convert biar pas save langsung sama dengan data sebeumnya
            try:
                int(values['ID_2'])
                values['Lahan_Perumahan'] = float(values['Lahan_Perumahan'])
                values['Lahan_Pertanian'] = float(values['Lahan_Pertanian'])
                values['Lahan_Perkebunan'] = float(values['Lahan_Perkebunan'])
                values['Sapi'] = int(values['Sapi'])
                values['Kambing'] = int(values['Kambing'])
                values['Ayam_Kampung'] = int(values['Ayam_Kampung'])
                values['Bebek'] = int(values['Bebek'])
                values['Itik'] = int(values['Itik'])
                values['Ayam_Petelur'] = int(values['Ayam_Petelur'])
                error_Non_numerik = False
            except ValueError:
                error_Non_numerik = True
            
            if error_Non_numerik: #If level 2: Cek numerik
                sg.popup('Ada rincian non numerik!')
                
            else:
                #3. Cek Range
                msg_element = [] #dummy list buat nampung error message
                msg='' #dummy value untuk simpen concatenate per element
                error_ID2 = len(values['ID_2']) != 4
                error_LahanPerumahan = values['Lahan_Perumahan'] < 0
                error_LahanPertanian = values['Lahan_Pertanian'] < 0
                error_LahanPerkebunan = values['Lahan_Perkebunan'] < 0
                error_Sapi = values['Sapi'] < 0
                error_Kambing = values['Kambing'] < 0
                error_AyamKampung = values['Ayam_Kampung'] < 0
                error_Bebek = values['Bebek'] < 0
                error_Itik = values['Itik'] < 0
                error_AyamPetelur = values['Ayam_Petelur'] < 0
                         
                if (error_ID2) or (error_LahanPerumahan) or (error_LahanPertanian) or (error_LahanPerkebunan) or (error_Sapi) or (error_Kambing) or (error_AyamKampung) or (error_Bebek) or (error_Itik) or (error_AyamPetelur): #If level 3 per variabel
                    if error_ID2:
                        msg_element.append('Jumlah Digit ID Keluarga tidak sama dengan 4!')
                    if error_LahanPerumahan:
                        msg_element.append('Lahan Perumahan tidak boleh negatif')
                    if error_LahanPertanian:
                        msg_element.append('Lahan Pertanian tidak boleh negatif')
                    if error_LahanPerkebunan:
                        msg_element.append('Lahan Perkebunan tidak boleh negatif')
                    if error_Sapi:
                        msg_element.append('Jumlah Sapi tidak boleh negatif')
                    if error_Kambing:
                        msg_element.append('Jumlah Kambing tidak boleh negatif')
                    if error_AyamKampung:
                        msg_element.append('Jumlah Ayam Kampung tidak boleh negatif')
                    if error_Bebek:
                        msg_element.append('Jumlah Bebek tidak boleh negatif')
                    if error_Itik:
                        msg_element.append('Jumlah Itik tidak boleh negatif')
                    if error_AyamPetelur:
                        msg_element.append('Jumlah Ayam Petelur tidak boleh negatif')
                    for i in msg_element:
                        msg += str(msg_element.index(i)+1) + '. ' + i + '\n'
                    sg.popup(msg)
                else:
                    values_ruta = {x: values[x] for x in values.keys() if x in
                                   ['ID_2','Lahan_Perumahan','Lahan_Pertanian','Lahan_Perkebunan',
                                    'Sapi','Kambing','Ayam_Kampung','Bebek','Itik','Ayam_Petelur']}
                    if values_ruta['ID_2'] in list(df_ruta['ID_2']):
                        sg.set_options(auto_size_buttons=True)
                        layout_konfirm_ind = [[sg.Text('Ubah Informasi Individu?', size=(16, 1))],
                                              [sg.Button('Ya'),sg.Button('Tidak')]
                                              ]
                        window1 = sg.Window('Individu dengan ID keluarga dan No ART sudah ada di database!', layout_konfirm_ind, auto_size_text=True)
                        try:
                            event,values = window1.read()
                            if event == 'Ya':
                                window1.close()
                                condition = df_ruta['ID_2'] == values_ruta['ID_2']
                                df_ruta[condition] = pd.DataFrame(values_ruta, index = df_ruta[condition].index.tolist())
                                df_ruta.to_excel('Database\Data Rumah Tangga.xlsx', index=False)
                                sg.popup('Data Keluarga Berhasil Diperbarui!')
                                clear_input()
                            if event =='Tidak':
                                window1.close()
                        except:
                            window1.close()                        
                    else:                           
                        values_ruta = {x: values[x] for x in values.keys() if x in ['ID_2','Lahan_Perumahan','Lahan_Pertanian','Lahan_Perkebunan','Sapi','Kambing','Ayam_Kampung','Bebek','Itik','Ayam_Petelur']}
                        df_ruta = df_ruta.append(values_ruta, ignore_index=True)
                        df_ruta.to_excel('Database\Data Rumah Tangga.xlsx', index=False)
                        sg.popup('Data Keluarga Tersimpan!')
                        clear_input()
          
        
window.close()
