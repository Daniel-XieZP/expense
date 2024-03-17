var addBtn = document.getElementById("add-btn");
var editBtns = document.querySelectorAll(".edit-btn");
var addForm = document.getElementById("add_expense");
var editForm = document.getElementById("edit_expense");
var delBtns = document.querySelectorAll(".del-btn");
var delForm = document.getElementById("delete_expense");
var modalTitle = document.getElementById("expense_label");


addBtn.onclick = function() {
    modalTitle.innerHTML = "Add";
    editForm.style.display = "none";
    addForm.style.display = "block";
    delForm.style.display = "none";
}

addForm.addEventListener("submit", function(event) {
    const ex_date = new Date(addForm.querySelector("#date").value).setHours(0, 0, 0, 0);
    const dt = new Date();
    const curr_date = new Date(dt.getFullYear() + "-" + (dt.getMonth() + 1) + "-" + dt.getDate());
    console.log("ex", ex_date);
    console.log("curr", curr_date); 
    if (ex_date > curr_date)
    {
        event.preventDefault();
        addForm.querySelector("#date").classList.add("error");
        alert("Expense date cannot be later than current date.");
    } else {
        addForm.querySelector("#date").classList.remove("error");
    }
})

editBtns.forEach(function(editBtn) {
    editBtn.onclick = function() {
        var row = this.closest("tr");
        var tds = row.querySelectorAll("td");
        var values = [];
        tds.forEach(function(td) {
            values.push(td.textContent.trim());
        });
        var id = editForm.querySelector("#expense_id");
        var select = editForm.querySelector("#category");
        var amount = editForm.querySelector("#amount");
        var ex_date = editForm.querySelector("#date");
        var desc = editForm.querySelector("#desc");
        id.value = values[0];
        optionToSelect = select.querySelector('option[value="' + values[1] + '"]');
        optionToSelect.selected = true;
        amount.value = values[2];
        ex_date.value = values[3];
        desc.value = values[4];
    
        modalTitle.innerHTML = "Edit"
        addForm.style.display = "none";
        editForm.style.display = "block";
        delForm.style.display = "none";
    }
})

delBtns.forEach(function(delBtn) {
    delBtn.onclick = function() {
        var id = delForm.querySelector("#expense_id");
        var row = this.closest("tr");
        var tds = row.querySelectorAll("td");
        id.value = tds[0].textContent.trim();

        modalTitle.innerHTML = "Delete"
        addForm.style.display = "none";
        editForm.style.display = "none";
        delForm.style.display = "block";
    }
})



