packages = {
    "250": {
        "w": "30",
        "m": "80"
    },
    "1000": {
        "w": "60",
        "m": "150"
    },
    "1500": {
        "w": "80",
        "m": "200"
    },
    "2500": {
        "w": "120",
        "m": "300"
    },
    "5000": {
        "w": "180",
        "m": "500"
    }
}
var timing = null
var plan = null
var email = null

var selectBtn = document.querySelector("select")
selectBtn.addEventListener("change", choose)
$("[purchase]").click(e => {
    plan = e.target.getAttribute("purchase")
    let t = undefined
    if (timing == "w") {
        t = "Weekly"
    } else if (timing == "m") {
        t = "Monthly"
    }
    $("[service]").html(t + " - " + plan + " Groups")
    $("[total-price]").html(packages[plan][timing])
})
function choose() {
    timing = selectBtn.value
    var obj_keys = Object.keys(packages)
    for (let i = 0; i < obj_keys.length; i++) {
        let price = document.querySelector(".price" + (i + 1))
        price.innerHTML = "$" + packages[obj_keys[i]][timing]
    }
}
choose()
$(".order").click(e => {
    e.preventDefault();
    email = $(".email-input").val() != "" ? $(".email-input").val() : null
    if (!(plan && timing && email && tgid != "")) return
    $(".order").prop("disabled", true)
    sendOrderRequest()
})
paymentMethodInput = document.querySelector(".payment-method")
$(".payment-method").change(e => {
    paymentMethod = paymentMethodInput.value
})

function sendOrderRequest() {
    fetch('/make-order', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ package: plan, timing, email, tgid, gateway: paymentMethod })
    })
        .then(response => response.json())
        .then(response => {
            if (response.startsWith("https://checkout.sellix.io/")){
                window.location.href = response
                return
            }
            alertUpdate(response, "danger")
        })
}

alertDiv = $("[alert]")
function alertUpdate(text, category){
    alertDiv.html(`<div class="alert alert-${category}" role="alert">${text}</div>`)
}