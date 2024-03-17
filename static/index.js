
var myChart;
var budgetChart;
var cat;
var amt;
var weekBtn = document.getElementById("week");
var monthBtn = document.getElementById("month");
var quarterBtn = document.getElementById("quarter");
var yearBtn = document.getElementById("year");
var customBtn = document.getElementById("custom");
var timeFrame = document.getElementById("time-frame");
var totalEx = document.getElementById("total-expenses");
var expenseBreakdownRows = document.getElementById("expense-breakdown").querySelector("tbody");
var customBtn = document.getElementById("customBtn");
var expenseBtn = document.getElementById("expenseBtn");
var budgetBtn = document.getElementById("budgetBtn");
var period = document.getElementById("period");
var exchart = document.getElementById("expenseChart");
var bdchart = document.getElementById("budget-view");
const bdsummary = document.getElementById("budget-summary");
const exsummary = document.getElementById("expense-summary");

function createOrUpdateExChart(cat, amt) {
    var ctx = document.getElementById("expenseChart").getContext("2d");
    
    if (myChart) {
        myChart.data.labels = cat;
        myChart.data.datasets[0].data = amt;
        myChart.data.datasets[0].backgroundColor = palette('tol', amt.length).map(function(hex) {
            return '#' + hex;
        })
        myChart.update();
    } else {
        myChart = new Chart(ctx, {
            type: 'doughnut', 
            data: {
                labels: cat,
                datasets: [{
                    label: 'Amount',
                    data: amt,
                    backgroundColor: palette('tol', amt.length).map(function(hex) {
                        return '#' + hex;
                    }),
                    hoverOffset: 4
                }]
            }
        });
    }
}

function createOrUpdateBdChart(cat, bud, amt = 0) {
    var ctx = document.getElementById("budget-view").getContext("2d");

    if (budgetChart) {
        budgetChart.data.labels = cat;
        budgetChart.data.datasets[0].data = bud;
        budgetChart.data.datasets[1].data = amt;
        budgetChart.update();
        console.log("update");
    } else {
        budgetChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: cat,
                datasets: [
                    {
                        label: 'Budget',
                        data: bud,
                        backgroundColor: "rgb(77, 166, 255)"
                    },
                    {
                        label: 'Amount Spent',
                        data: amt,
                        backgroundColor: "rgb(255, 153, 153)"
                    }
                ]
            }
        })
    }
}

document.addEventListener("DOMContentLoaded", function() {
    expenseBtn.click();
});

weekBtn.addEventListener("click", function() {
    $.ajax({
        type: "GET",
        url: "/sort/week",
        success: function(response) {
            var res = response;
            cat = res['cat'];
            amt = res['amt'];
            createOrUpdateExChart(cat, amt);
            timeFrame.innerHTML = res['sDate'] + " - " + res['eDate'];
            totalEx.innerHTML = "$" + res['tt_expense'];
            expenseBreakdownRows.innerHTML = "";
            for (let i = 0; i < cat.length; i++) {
                var tableRow = document.createElement("tr");
                var td1 = document.createElement("td");
                var td2 = document.createElement("td");
                td1.innerHTML = cat[i];
                td2.innerHTML = amt[i];
                tableRow.appendChild(td1);
                tableRow.appendChild(td2);
                expenseBreakdownRows.appendChild(tableRow);
            }
        },
        error: function() {
            alert("error displaying chart");
        }
    })
});

monthBtn.addEventListener("click", function() {
    $.ajax({
        type: "GET",
        url: "/sort/month",
        success: function(response) {
            var res = response;
            cat = res['cat'];
            amt = res['amt'];
            createOrUpdateExChart(cat, amt);
            timeFrame.innerHTML = res['sDate'] + " - " + res['eDate'];
            totalEx.innerHTML = "$" + res['tt_expense'];
            expenseBreakdownRows.innerHTML = "";
            for (let i = 0; i < cat.length; i++) {
                var tableRow = document.createElement("tr");
                var td1 = document.createElement("td");
                var td2 = document.createElement("td");
                td1.innerHTML = cat[i];
                td2.innerHTML = amt[i];
                tableRow.appendChild(td1);
                tableRow.appendChild(td2);
                expenseBreakdownRows.appendChild(tableRow);
            }
        },
        error: function() {
            alert("error displaying chart");
        }
    })
});

quarterBtn.addEventListener("click", function() {
    $.ajax({
        type: "GET",
        url: "/sort/quarter",
        success: function(response) {
            var res = response;
            cat = res['cat'];
            amt = res['amt'];
            createOrUpdateExChart(cat, amt);
            timeFrame.innerHTML = res['sDate'] + " - " + res['eDate'];
            totalEx.innerHTML = "$" + res['tt_expense'];
            expenseBreakdownRows.innerHTML = "";
            for (let i = 0; i < cat.length; i++) {
                var tableRow = document.createElement("tr");
                var td1 = document.createElement("td");
                var td2 = document.createElement("td");
                td1.innerHTML = cat[i];
                td2.innerHTML = amt[i];
                tableRow.appendChild(td1);
                tableRow.appendChild(td2);
                expenseBreakdownRows.appendChild(tableRow);
            }
        },
        error: function() {
            alert("error displaying chart");
        }
    })
});

yearBtn.addEventListener("click", function() {
    $.ajax({
        type: "GET",
        url: "/sort/year",
        success: function(response) {
            var res = response;
            cat = res['cat'];
            amt = res['amt'];
            createOrUpdateExChart(cat, amt);
            timeFrame.innerHTML = res['sDate'] + " - " + res['eDate'];
            totalEx.innerHTML = "$" + res['tt_expense'];
            expenseBreakdownRows.innerHTML = "";
            for (let i = 0; i < cat.length; i++) {
                var tableRow = document.createElement("tr");
                var td1 = document.createElement("td");
                var td2 = document.createElement("td");
                td1.innerHTML = cat[i];
                td2.innerHTML = amt[i];
                tableRow.appendChild(td1);
                tableRow.appendChild(td2);
                expenseBreakdownRows.appendChild(tableRow);
            }
        },
        error: function() {
            alert("error displaying chart");
        }
    })
});

customBtn.addEventListener("click", function() {
    var sDate = document.getElementById("sDate").value;
    var eDate = document.getElementById("eDate").value;
    $.ajax({
        type: "POST",
        url: "/sort/custom",
        data: JSON.stringify({ "sDate" : sDate, "eDate" : eDate}),
        contentType: "application/json",
        success: function(response) {
            var res = response;
            cat = res['cat'];
            amt = res['amt'];
            createOrUpdateExChart(cat, amt);
            timeFrame.innerHTML = res['sDate'] + " - " + res['eDate'];
            totalEx.innerHTML = "$" + res['tt_expense'];
            expenseBreakdownRows.innerHTML = "";
            for (let i = 0; i < cat.length; i++) {
                var tableRow = document.createElement("tr");
                var td1 = document.createElement("td");
                var td2 = document.createElement("td");
                td1.innerHTML = cat[i];
                td2.innerHTML = amt[i];
                tableRow.appendChild(td1);
                tableRow.appendChild(td2);
                expenseBreakdownRows.appendChild(tableRow);
            }
        }, error: function() {
            alert("error displaying chart");
        }
    })
});

budgetBtn.addEventListener("click", function() {

    $.ajax({
        type: "GET",
        url: "/budgetview",
        success: function(response) {
            var res = response;
            createOrUpdateBdChart(res['cat'], res['bud'], res['amt']);
            var rbudget = document.getElementById("rbudget").querySelector("tbody");
            var ebudget = document.getElementById("ebudget").querySelector("tbody");
            rbud = res['rbud'];
            ebud = res['ebud'];
            rbudget.innerHTML = "";
            ebudget.innerHTML = "";
            for (let key in rbud) {
                var tr = document.createElement("tr");
                var td1 = document.createElement("td");
                var td2 = document.createElement("td");
                td1.innerHTML = key;
                td2.innerHTML = rbud[key];
                tr.appendChild(td1);
                tr.appendChild(td2);
                rbudget.appendChild(tr);
            }
            for (let key in ebud) {
                var tr = document.createElement("tr");
                var td1 = document.createElement("td");
                var td2 = document.createElement("td");
                td1.innerHTML = key;
                td2.innerHTML = ebud[key];
                td2.style.color = "#ff0033";
                tr.appendChild(td1);
                tr.appendChild(td2);
                ebudget.appendChild(tr);
            }
        }, error: function() {
            "error creating budgetview";
        }
    })

    exchart.style.display = "none";
    period.style.display = "none";
    bdchart.style.display = "block";
    bdsummary.style.display = "block";
    exsummary.style.display = "none";
});

expenseBtn.addEventListener("click", function() {

    weekBtn.click();

    period.style.display = "inline-flex";
    exchart.style.display = "block";
    exsummary.style.display = "block";
    bdsummary.style.display = "none";
    bdchart.style.display = "none";
});