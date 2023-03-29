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
timing = null
group = null
selectBtns = document.querySelectorAll("select")
price = document.querySelector("price")
selectBtns.forEach(select => {
  select.addEventListener("change", e => {
    if (select.name == "package") {
      group = select.value
    }
    else if (select.name == "timing") {
      timing = select.value
    }

    if (!(group && timing)) return

    price.innerHTML = packages[group][timing]
  })
})
