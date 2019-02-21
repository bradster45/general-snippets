import requests

def recaptcha_request(request):
    google_recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret':'6LcUVyQUAAAAACs0P26wqUBgrkDroyNfyGMPCetr',
        'response':request.POST.get('g-recaptcha-response'),
    }
    return requests.post(google_recaptcha_url, data=data)

'''
    CALL FUNCTION ASSIGNED TO VARIABLE
    r = recaptcha_request(request)

    IF USER HAS PASSSED RECAPTCHA
    if r.json().get('success') == True:
        SUCCESS CODE
    else:
        RAISE/RETURN THAT THE USER HAS FAILED RECAPTCHA

        
<script src='https://www.google.com/recaptcha/api.js'></script>
<div class="g-recaptcha" data-sitekey="6LcUVyQUAAAAAHLR57m4CKdmLkFXnGho75painXi"></div>
'''

