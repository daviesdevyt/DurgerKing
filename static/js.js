var timing = null
var plan = null
var email = null

btnFrequency = $("[btn-frequency]")

btnFrequency.click(e => {
    current = btnFrequency.data("freq")
    if (current == "w") {
        btnFrequency.data("freq", "m")
        btnFrequency.html("Monthly")
    }
    else if (current == "m") {
        btnFrequency.data("freq", "w")
        btnFrequency.html("Weekly")
    }
    choose()
})

$("#pricing .pricing-tables").click(e => {
    let plan = e.currentTarget.getAttribute("purchase")
    console.log(plan)
    let t = undefined
    if (timing == "w") {
        t = "Weekly"
    } else if (timing == "m") {
        t = "Monthly"
    }
    $("[service]").html(t + " - " + plan + " Groups")
    $("[total-price]").html(packages[plan][timing])
})

var obj_keys = Object.keys(packages)
function choose() {
    timing = btnFrequency.data("freq")
    for (let i = 0; i < obj_keys.length; i++) {
        let price = document.querySelector(".price" + i)
        price.innerHTML = "$" + packages[obj_keys[i]][timing]
    }
}
choose()
$(".order").click(e => {
    e.preventDefault();
    email = $(".email-input").val() != "" ? $(".email-input").val() : null
    if (!(plan && timing && email && tgid != "")) return
    $(".order").prop("disabled", true)
    $(".order").html("Loading ...")
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
        .then(response => {
            if (!response.ok) throw new Error()
            return response.json()
        })
        .then(response => {
            if (response.startsWith("https://checkout.sellix.io/")) {
                window.location.href = response
                return
            }
            alertUpdate(response, "danger")
            throw new Error()
        })
        .catch(err => {
            $(".order").prop("disabled", false)
            $(".order").html("Purchase")
        })
}

alertDiv = $("[alert]")
function alertUpdate(text, category) {
    alertDiv.html(`<div class="alert alert-${category}" role="alert">${text}</div>`)
}