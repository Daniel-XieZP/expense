var addForm = document.getElementById("add_budget");
var addBtn = document.getElementById("add-btn");
var editForm = document.getElementById("edit_budget");
var editBtns = document.getElementsByClassName("edit-btn");
var delBtns = document.getElementsByClassName("del-btn");
var delForm = document.getElementById("delete_budget");
var modalTitle = document.getElementById("budget_label");

addBtn.onclick = function() {
    modalTitle.innerHTML = "Add";
    addForm.style.display = "block";
    editForm.style.display = "none";
    delForm.style.display = "none";
}

addForm.addEventListener("submit", function(event) {
    const startDate = new Date(addForm.querySelector("#date_start").value);
    const endDate = new Date(addForm.querySelector("#date_end").value);

    if (endDate < startDate) {
        event.preventDefault();
        addForm.querySelector("#date_end").classList.add("error");
        alert("End date cannot be earlier than start date.");
    } else {
        addForm.querySelector("date_end").classList.remove("error");
    }
})

Array.from(editBtns).forEach(function(editBtn) {
    editBtn.onclick = function() {
        var row = this.closest("tr");
        var tds = row.querySelectorAll("td");
        var values = [];
        tds.forEach(function(td) {
            values.push(td.textContent.trim());
        });
        var id = editForm.querySelector("#budget_id");
        var amount = editForm.querySelector("#amount");
        var sDate = editForm.querySelector("#date_start");
        var eDate = editForm.querySelector("#date_end");
        var category = editForm.querySelector("#category");
        id.value = values[0];
        optionToSelect = category.querySelector('option[value="' + values[1] + '"]');
        optionToSelect.selected = true;
        amount.value = values[2];
        sDate.value = values[3];
        eDate.value = values[4];

        modalTitle.innerHTML = "Edit";
        addForm.style.display = "none";
        editForm.style.display = "block";
        delForm.style.display = "none";
    }
})

editForm.addEventListener("submit", function(event) {
    const startDate = new Date(editForm.querySelector("#date_start").value);
    const endDate = new Date(editForm.querySelector("#date_end").value);

    if (endDate < startDate) {
        event.preventDefault();
        editForm.querySelector("#date_end").classList.add("error");
        alert("End date cannot be earlier than start date.");
    } else {
        editForm.querySelector("#date_end").classList.remove("error");
    }
})


Array.from(delBtns).forEach(function(delBtn) {
    delBtn.onclick = function() {
        var row = this.closest("tr");
        tds = row.querySelectorAll("td");
        var budget_id = delForm.querySelector("#budget_id");
        budget_id.value = tds[0].textContent.trim();

        modalTitle.innerHTML = "Delete";
        addForm.style.display = "none";
        editForm.style.display = "none";
        delForm.style.display = "block";
    }
})