import os


def simple(info):
    print("Trying to print HTML")
    html = '''
        <!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <div><img class="float-right" src=https://ooldigital.com/wp-content/uploads/2019/08/Ool_isotipo_redwhite_03.png></img></div>
        <div class="container mt-5">
    '''
    html += f'<div class="h1 mt-5 lighter">Metadata</div>'

    html += '<div class="mt-5">'
    html += f'<div class="row"><div class="h3 lighter">{"Campaign"}: <div class="h4 darker ml-3">{info["campaign"]["name"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Agency"}: <div class="h4 darker ml-3">{info["campaign"]["agency"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Type"}: <div class="h4 darker ml-3">{info["data"]["type"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Shotcode"}: <div class="h4 darker ml-3">{info["data"]["shots"]["code"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Created"}: <div class="h4 darker ml-3">{info["created_at"]}</div></div></div>'
    html += '</div>'

    html += '''
            </div>
        </body>
        <style>
            .darker{
                color: rgb(100,100,100)
            }
            .lighter{
                color:rgb(200,200,200)
            }
            body{
                background-color: rgb(30,30,30)
            }
        </style>
    </html>'''

    return html


def composed(info):
    projects = info["data"]["subprojects"]
    html = '''
        <!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <div><img class="float-right" src=https://ooldigital.com/wp-content/uploads/2019/08/Ool_isotipo_redwhite_03.png></img></div>
        <div class="container mt-5">
    '''
    html += f'<div class="h1 mt-5 lighter">Metadata</div>'

    html += '<div class="mt-5">'
    html += f'<div class="row"><div class="h3 lighter">{"Campaign"}: <div class="h4 darker ml-3">{info["campaign"]["name"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Agency"}: <div class="h4 darker ml-3">{info["campaign"]["agency"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Type"}: <div class="h4 darker ml-3">{info["data"]["type"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Created"}: <div class="h4 darker ml-3">{info["created_at"]}</div></div></div>'
    html += f'<div class="row"><div class="h3 lighter">{"Projects"}:</div></div>'
    html += '''
        <table class="table table-bordered table-dark">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Shotcode</th>
                <th scope="col">Path</th>
                </tr>
            </thead>
            <tbody>
    '''

    for number, project in enumerate(projects, 1):
        html += '<tr>'
        html += f'<th scope="row">{number}</th>'
        html += f'<td>{project["name"]}</td>'
        html += f'<td>{project["shots"]["code"]}</td>'
        html += f'<td>{os.path.normpath(os.path.join(info["path"], "Projects",project["name"]))}</td>'
        html += '</tr>'

    html += '</tbody></table>'
    html += '</div>'
    html += '''
            </div>
        </body>
        <style>
            .darker{
                color: rgb(100,100,100)
            }
            .lighter{
                color:rgb(200,200,200)
            }
            body{
                background-color: rgb(30,30,30)
            }
        </style>
    </html>'''

    return html
