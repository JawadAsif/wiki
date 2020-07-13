from django.shortcuts import render, HttpResponseRedirect, reverse
from . import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    if entry:
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/entry_not_found.html")


def search(request):
    if request.method == "POST":
        print("here")
        searched_text = request.POST["q"]
        print(searched_text)
        entries = [entry.lower() for entry in util.list_entries()]
        print(entries)
        if searched_text in entries:
            return HttpResponseRedirect(reverse("entry",kwargs={'title': searched_text}))
        else:
            result = [s for s in entries if searched_text in s]
            print(result)
            return render(request, "encyclopedia/searched_result.html", {
                          "results": result
                          })
