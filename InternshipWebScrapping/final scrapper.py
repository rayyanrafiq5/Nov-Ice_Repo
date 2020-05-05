import requests
import lxml.html
home_url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'

again = True
while again:
    r = requests.get(url=home_url)
    doc = lxml.html.fromstring(r.content)
    cookies = r.cookies
    viewstate = doc.xpath('//input[@name="javax.faces.ViewState"]/@value')[0]



    def get_captcha():
        imageurlext = doc.xpath('//img[@id="form_rcdl:j_idt34:j_idt41"]/@src')[0]
        imageurl="https://parivahan.gov.in"+str(imageurlext)
        imgobj=requests.get(imageurl)
        with open('capcha.jpg', 'wb') as f:
            f.write(imgobj.content)
        captcha=input('Captcha: ')
        return captcha


    print("               =>SS-RRYYYYNNNNNNN OR SSRR YYYYNNNNNNN")
    dlno = input("Enter your dlno: ").upper()

    print("              =>DD-MM-YYYY")
    dl_owner_DOB = input("Enter your DOB: ").replace('/','-')

    captcha = get_captcha()

    my_dict = {
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'form_rcdl:j_idt46',
        'javax.faces.partial.execute': "@all",
        "javax.faces.partial.render": "form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl",
        "form_rcdl:j_idt46": "form_rcdl:j_idt46",
        "form_rcdl": "form_rcdl",
        "form_rcdl:tf_dlNO": dlno,
        "form_rcdl:tf_dob_input": dl_owner_DOB,
        "form_rcdl:j_idt34:CaptchaID": captcha,
        'javax.faces.ViewState': viewstate,

    }

    a = requests.post(url=home_url, data=my_dict, cookies=cookies)

    tree = lxml.html.fromstring(a.content)

    key = tree.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered']/tr[*]/td/span[@class='font-bold']/text()")
    val = tree.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered']/tr[*]/td/span[@class='']/text()")
    value = tree.xpath('//table[@class="table table-responsive table-striped table-condensed table-bordered"]/tr[*]/td/text()')

    for i in value:
            val.append(i)

    table2_key = tree.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered data-table']/tr/td/span[@class='font-bold']/text()")
    table2_val = tree.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered data-table']/tr/td/text()")
    try:
        table2_keys_key = ['Non-Transport','Transport']
        table2_key.remove('Non-Transport')
        table2_key.remove('Transport')
        json_dict = {}

        for i in range(len(key)):
            json_dict.update({key[i][0:-1]:val[i]})

        json_dict.update({table2_keys_key[0]:{table2_key[0][0:-2]:table2_val[0],
                                              table2_key[1][0:-2]:table2_val[1]},
                          table2_keys_key[1]:{table2_key[2][0:-2]:table2_val[2],
                                              table2_key[3][0:-2]:table2_val[3]},
                          table2_key[4]:table2_val[4],
                          table2_key[5]:table2_val[5]}

                         )

        dyn_heading = tree.xpath('//span[@class="ui-column-title"]/text()')

        dyn_value = tree.xpath('//td[@role="gridcell"]/text()')

        cov_dict = {}

        for i in range(len(dyn_value)//3):
            cov_dict.update({i+1:{dyn_heading[0]:dyn_value[0+3*i],dyn_heading[1]:dyn_value[1+3*i],dyn_heading[2]:dyn_value[2+3*i]}})
        json_dict.update({'class of vehical details':cov_dict})

        import json

        final_json = json.dumps(json_dict, indent=2)
        print(final_json)
        again = False
    except(ValueError,IndexError):
        print('No DL Details Found!'
              'Enter The Details Again.')
        again = True