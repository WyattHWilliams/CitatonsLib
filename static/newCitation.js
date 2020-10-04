const summary = document.querySelector('div[id="summary"]');


// adjust indices when forms are removed
function adjustIndices(removedIndex, formClass) {
    const forms = document.querySelectorAll(formClass);

    forms.forEach(function (form) {
        // console.log(form)
        const index = parseInt(form.dataset.index);
        const newIndex = index - 1;

        if (index < removedIndex) {
            return True;
        }

        // Change the Id in the form
        form.setAttribute('id', form.getAttribute('id').replace(index, newIndex));
        form.dataset.index = newIndex;

        // Change Ids for form inputs
        form.querySelectorAll('input').forEach(function (input) {
            input.setAttribute('id', input.getAttribute('id').replace(index, newIndex));
            input.setAttribute('name', input.getAttribute('name').replace(index, newIndex));
        });
    });
}

// remove a subform
function removeForm(form, formClass) {
    const removedIndex = parseInt(form.dataset.index);

    form.remove();
    adjustIndices(removedIndex, formClass);
}

// add a subform


summary.addEventListener('click', function (e) {
    // console.log(e.target);
    if (e.target.classList.contains('remove_ent')) {
        form = e.target.parentElement
        formClass = '.entform'
        removeForm(form, formClass);
    }
    else if (e.target.classList.contains('remove_sec')) {
        form = e.target.parentElement
        formClass = '.secform'
        removeForm(form, formClass);
    }
})