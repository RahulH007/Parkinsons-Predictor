from django import forms

class ParameterForm(forms.Form):
    # Define your fields here
    field1 = forms.FloatField(label='Field 1')
    field2 = forms.FloatField(label='Field 2')
    # Add more fields as needed

class HospitalParameterForm(forms.Form):
    mdvp_fo = forms.FloatField(label='MDVP:Fo(Hz)')
    mdvp_fhi = forms.FloatField(label='MDVP:Fhi(Hz)')
    mdvp_flo = forms.FloatField(label='MDVP:Flo(Hz)')
    mdvp_jitter_percent = forms.FloatField(label='MDVP:Jitter(%)')
    mdvp_jitter_abs = forms.FloatField(label='MDVP:Jitter(Abs)')
    mdvp_rap = forms.FloatField(label='MDVP:RAP')
    mdvp_ppq = forms.FloatField(label='MDVP:PPQ')
    jitter_ddp = forms.FloatField(label='Jitter:DDP')
    mdvp_shimmer = forms.FloatField(label='MDVP:Shimmer')
    mdvp_shimmer_db = forms.FloatField(label='MDVP:Shimmer(dB)')
    shimmer_apq3 = forms.FloatField(label='Shimmer:APQ3')
    shimmer_apq5 = forms.FloatField(label='Shimmer:APQ5')
    mdvp_apq = forms.FloatField(label='MDVP:APQ')
    shimmer_dda = forms.FloatField(label='Shimmer:DDA')
    nhr = forms.FloatField(label='NHR')
    hnr = forms.FloatField(label='HNR')
    rpde = forms.FloatField(label='RPDE')
    dfa = forms.FloatField(label='DFA')
    spread1 = forms.FloatField(label='spread1')
    spread2 = forms.FloatField(label='spread2')
    d2 = forms.FloatField(label='D2')
    ppe = forms.FloatField(label='PPE')
