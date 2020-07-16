from . import util
from . import markdown2
from django.shortcuts import render, HttpResponseRedirect, reverse, \
    HttpResponse
from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content", widget=forms.Textarea)


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
        searched_text = request.POST["q"]
        # searched_text_lower = searched_text.lower()
        # print(searched_text)
        entries = util.list_entries()
        # entries_lower = [entry.lower() for entry in entries]
        # print(entries)
        # if searched_text_lower in entries_lower:
        if searched_text in entries:
            return HttpResponseRedirect
            (reverse("entry",
                     kwargs={'title': searched_text}))
        else:
            # results = [s.capitalize() for s in entries_lower \
            # if searched_text_lower in s]
            results = [s for s in entries if searched_text in s]
            # print(results)
            return render(request, "encyclopedia/searched_result.html", {
                          "results": results,
                          "searched_text": searched_text
                          })


def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            print(title)
            content = form.cleaned_data["content"]
            print(content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })
