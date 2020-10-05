const summary = document.querySelector('div[id="summary"]');


// adjust indices when forms are removed
function adjustIndices(removedIndex, formClass) {
    const forms = document.querySelectorAll(formClass);

    forms.forEach(function (form) {
        // console.log(form)
        const index = parseInt(form.dataset.index);
        const newIndex = index - 1;

        if (index < removedIndex) {
            return true;
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

// add an entry form
function addEntForm(secIdx) {
    const temp_ent_form = document.querySelector('div[id="entry-*"]')
    if (!temp_ent_form) {
        console.log('[ERROR] Cannot Find Template');
        return;
    }
    const section = document.querySelector(`div[id="section-${secIdx}"]`);
    const entFormsContainer = document.querySelector('div[id="entforms-container"]');
    const lastEntForm = document.querySelector(`div[id="entforms-container"] > :last-child`);
    console.log(lastEntForm)

    let newIndex = 0;

    if (lastEntForm) {
        newIndex = parseInt(lastEntForm.dataset.index) + 1;
    }

    //add elements
    let newForm = temp_ent_form.cloneNode(true);

    newForm.setAttribute('id', newForm.getAttribute('id').replace('*', newIndex));
    newForm.dataset.index = newIndex;

    newForm.querySelectorAll('input').forEach(function (input) {
        input.setAttribute('id', input.getAttribute('id').replace('*', newIndex));
        input.setAttribute('id', input.getAttribute('id').replace('^', secIdx));
        input.setAttribute('name', input.getAttribute('name').replace('*', newIndex));
        input.setAttribute('name', input.getAttribute('name').replace('^', secIdx));
    });

    //append
    entFormsContainer.appendChild(newForm);
    newForm.classList.add('entForm');
    newForm.classList.remove('is-hidden');
}

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

summary.addEventListener('click', function (e) {
    // console.log(e.target);
    if (e.target.classList.contains('add_ent')) {
        secIdx = e.target.parentElement.dataset.index;
        console.log(secIdx);
        addEntForm(secIdx);
    }
})