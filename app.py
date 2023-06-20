from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)



@app.route('/')
def index():
    with open("blog_data.json", "r") as json_file:
        blog_data = json.load(json_file)

        stored_blog_posts = []

        for blog in range(len(blog_data)):
            stored_blog_posts.append(blog_data[blog])

        # reorders the blog posts so that the newer posts are shown first
        reversed_list = reversed(stored_blog_posts)
        reversed_order = list(reversed_list)
        reversed_blog_order = {}

        for blog in reversed_order:
            name = blog.pop("id")
            reversed_blog_order[name] = blog

    return render_template('index.html', posts=reversed_blog_order)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":

        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        with open("blog_data.json", "r") as data:
            blog_data = json.load(data)
            unique_id = 1

            # gets an ID number that has never been used on the blog.
            for new_id in blog_data:
                if new_id["id"] == unique_id:
                    unique_id += 1
                    continue

            # makes a new dictionairy
            new_post = {"id": unique_id, "author": author, "title": title, "content": content}

            with open("blog_data.json", "w") as new_file:
                blog_data.append(new_post)
                print(blog_data)
                json.dump(blog_data, new_file)

            return redirect(url_for("index"))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        pass
    # Update the post in the JSON file
    # Redirect back to index

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route("/delete", methods=["GET","POST"])
def delete():
    if request.method == "POST":
        with open("blog_data.json", "r") as data:
            blog_data = json.load(data)

            checked_posts = []

            #checks if checkbox is applied
            for checkbox in range(len(blog_data)):
                delete_post = request.form.get(f"checkbox_value{blog_data[checkbox]['id']}")
                if delete_post:
                    checked_posts.append(blog_data[checkbox])

            #deletes selected posts from json file
            for delete in range(len(checked_posts)):
                blog_data.remove(checked_posts[delete])

            with open("blog_data.json", "w") as new_file:
                json.dump(blog_data, new_file)

            return redirect(url_for("index"))



    with open("blog_data.json", "r") as json_file:
        blog_data = json.load(json_file)

        stored_blog_posts = []

        for blog in range(len(blog_data)):
            stored_blog_posts.append(blog_data[blog])

        # reorders the blog posts so that the newer posts are shown first
        reversed_list = reversed(stored_blog_posts)
        reversed_order = list(reversed_list)
        reversed_blog_order = {}

        for blog in reversed_order:
            name = blog.pop("id")
            reversed_blog_order[name] = blog

        return render_template("delete.html", posts=reversed_blog_order)



@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000, debug=True)

