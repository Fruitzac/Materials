import csv
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def home():
    with open('ProductsApp/products.txt' , 'r') as p:
        products_list = []
        products_listraw = csv.reader(p)
        #Clean up the csv reader list as for some reason the html detects whitespaces 
        # thus cannot access the images 
        for row in products_listraw:
            product_row =[]
            for i in row:
                product_row.append(i.strip())
            products_list.append(product_row)
        return render_template('products.html', products = products_list)

@app.route('/product')
def view():
    return render_template('product_frm.html')

@app.route('/add' , methods=['POST'])
def add_product():
    image_file_name = ''

    if 'image' in request.files:
        image_file = request.files["image"]
        image_file_name = image_file.filename
        image_file.save("ProductsApp/static/images/" + image_file_name)
    
    name = (request.form['name'])
    description = (request.form['description'])
    price = (request.form['price'])
    image = image_file_name
    with open('ProductsApp/products.txt', 'a') as p:
        p.write("\n" + f"{name}, {description}, {price}, {image}")

    return redirect('/')    

if __name__ == '__main__':
    app.run()
