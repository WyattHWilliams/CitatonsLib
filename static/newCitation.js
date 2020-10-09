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
    const temp_ent_form = document.querySelector('div[id="section-^-entry-*"]')
    if (!temp_ent_form) {
        console.log('[ERROR] Cannot Find Template');
        return;
    }
    const section = document.querySelector(`div[id="section-${secIdx}"]`);
    const entFormsContainer = document.querySelector(`div[id="entforms-container-${secIdx}"]`);
    const entforms = document.querySelectorAll('div[class="entform"]');
    const lastEntForm = entforms[entforms.length - 1]
    // const lastEntForm = document.querySelector(`div[id="entforms-container-${secIdx}"] > :last-child`);
    console.log(lastEntForm)

    let newIndex = 0;

    if (lastEntForm) {
        newIndex = parseInt(lastEntForm.dataset.index) + 1;
    }

    //add elements
    let newForm = temp_ent_form.cloneNode(true);

    newForm.setAttribute('id', newForm.getAttribute('id').replace('*', newIndex));
    newForm.setAttribute('id', newForm.getAttribute('id').replace('^', secIdx));
    newForm.dataset.index = newIndex;

    newForm.querySelectorAll('input').forEach(function (input) {
        input.setAttribute('id', input.getAttribute('id').replace('*', newIndex));
        input.setAttribute('id', input.getAttribute('id').replace('^', secIdx));
        input.setAttribute('name', input.getAttribute('name').replace('*', newIndex));
        input.setAttribute('name', input.getAttribute('name').replace('^', secIdx));
    });

    newForm.querySelectorAll('label').forEach(function (label) {
        label.setAttribute('for', label.getAttribute('for').replace('*', newIndex));
        label.setAttribute('for', label.getAttribute('for').replace('^', secIdx));
    });

    //append
    entFormsContainer.appendChild(newForm);
    newForm.classList.add('entform');
    newForm.classList.remove('is-hidden');
}

// add an entry form
function addSecForm() {
    const temp_sec_form = document.querySelector('div[id="section-^"]')
    if (!temp_sec_form) {
        console.log('[ERROR] Cannot Find Template');
        return;
    }
    const secFormsContainer = document.querySelector('div[id="secforms-container"]');
    const lastSecForm = document.querySelector(`div[id="secforms-container"] > :last-child`);
    console.log(lastSecForm)

    let newIndex = 0;

    if (lastSecForm) {
        newIndex = parseInt(lastSecForm.dataset.index) + 1;
    }

    //add elements
    let newForm = temp_sec_form.cloneNode(true);

    newForm.setAttribute('id', newForm.getAttribute('id').replace('^', newIndex));
    newForm.dataset.index = newIndex;

    newForm.querySelectorAll('input').forEach(function (input) {
        input.setAttribute('id', input.getAttribute('id').replace('^', newIndex));
        input.setAttribute('name', input.getAttribute('name').replace('^', newIndex));
    });

    newForm.querySelectorAll('label').forEach(function (label) {
        label.setAttribute('for', label.getAttribute('for').replace('^', newIndex));
    });

    // newForm.querySelectorAll('form').forEach(function (form) {
    //     form.setAttribute('id', form.getAttribute('id').replace('^', newIndex));
    // });

    newForm.querySelectorAll('div[class="entforms-cont"]').forEach(function (div) {
        div.setAttribute('id', div.getAttribute('id').replace('^', newIndex));
    });

    //append
    secFormsContainer.appendChild(newForm);
    newForm.classList.add('secform');
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
    else if (e.target.classList.contains('add_sec')) {
        addSecForm();
    }
})