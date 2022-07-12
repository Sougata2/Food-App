'use strict'
const orders = []
// Cart System , page : FoodSection.
const choices = []
// let display = document.querySelector('.display-choice')
const choice_table = document.querySelector('.choice-table tbody')

//Toggle Cart
document.querySelector('.show-cart').addEventListener('click', function () {
    document.querySelector('.cart').classList.toggle('hidden')
})


for (let i = 1; i <= 6; i++) {

    let btn = document.querySelector(`.btn--${i}`)
    let foodName = document.querySelector(`.food-name--${i}`)
    let price = document.querySelector(`.price--${i}`)

    btn.addEventListener('click',

        function () {
            if (!choices.includes(foodName.textContent) && choices.length < 3) {
                // prerequisites
                document.querySelector('.empty-cart').classList.add('hidden')
                document.querySelector('.confirm').classList.remove('hidden')
                document.querySelector('.display-choice').classList.remove('hidden')
                // document.querySelector('.clear-cart').classList.remove('hidden')


                choices.push(foodName.textContent)

                // create element (table row , table data , buttons )
                const tr = document.createElement('tr')
                const td_name = document.createElement('td')
                const td_price = document.createElement('td')
                const td_quantity = document.createElement('td')
                const td_add = document.createElement('td')
                const td_remove = document.createElement('td')
                const add_button = document.createElement('button')
                const remove_button = document.createElement('button')

                // create node element (food name, price, quantity, add_button , remove_button)
                const node_name = document.createTextNode(foodName.textContent)
                const node_price = document.createTextNode(price.textContent)
                const node_quantity = document.createTextNode('1')
                const node_add = document.createTextNode('+')
                const node_remove = document.createTextNode('x')

                // add node to element.
                td_name.appendChild(node_name)
                td_price.appendChild(node_price)
                td_quantity.appendChild(node_quantity)
                add_button.appendChild(node_add)
                remove_button.appendChild(node_remove)
                td_add.appendChild(add_button)
                td_remove.appendChild(remove_button)


                // add table data to table row
                tr.appendChild(td_name)
                tr.appendChild(td_price)
                tr.appendChild(td_quantity)
                tr.appendChild(td_add)
                tr.appendChild(td_remove)

                // add table row to the table.
                choice_table.appendChild(tr)

                // attach the respective classes.
                tr.classList.add('order-row')
                tr.classList.add('choice-row')
                td_name.classList.add('choice-col')
                td_price.classList.add('choice-col')
                td_quantity.classList.add('choice-col')
                td_add.classList.add('choice-col')
                td_remove.classList.add('choice-col')
                td_add.classList.add('add-col')
                td_remove.classList.add(`remove-col`)

                // add Quantity
                add_button.addEventListener('click', function () {
                    if (Number(td_quantity.textContent) < 10) {
                        let value = Number(td_quantity.textContent)
                        value++
                        td_quantity.textContent = String(value)
                    }
                })
                // remove table data
                remove_button.addEventListener('click', function () {
                    removeOrderedFood(td_name.textContent)
                    tr.remove()
                })
            }
        })
}

// remove the specific element from the choices.
const removeOrderedFood = function (foodName) {
    const del_index = choices.indexOf(foodName)
    choices.splice(del_index, 1)
    if (!choices.length) {
        document.querySelector('.empty-cart').classList.remove('hidden')
        document.querySelector('.display-choice').classList.add('hidden')
        document.querySelector('.confirm').classList.add('hidden')
        // document.querySelector('.clear-cart').classList.add('hidden')
    }
}

// Clear the cart  TODO: to be completed
// document.querySelector('.clear-cart').addEventListener('click', function (){
//     choices.splice(0)
//     document.querySelector('.empty-cart').classList.remove('hidden')
//     document.querySelector('.display-choice').classList.add('hidden')
//     document.querySelector('.confirm').classList.add('hidden')
//     document.querySelector('.clear-cart').classList.add('hidden')
// })


// TODO: ADD IT LATER
// document.querySelector('.confirm').addEventListener('click', function () {
//     for (let i = 0; i < document.querySelectorAll('.order-row').length; i++) {
//         const orderDetails = []
//         for (let j = 0; j < 3; j++) {
//             console.log(document.querySelectorAll('.order-row')[i].childNodes[j].textContent)
//             orderDetails.push(document.querySelectorAll('.order-row')[i].childNodes[j].textContent)
//         }
//         orders.push(orderDetails)
//     }
// })


// document.querySelectorAll('.order-row')[i].childNodes.length

const getData = function () {
    for (let i = 0; i < orders.length; i++) {
        document.querySelector(`.food--${i}`).value = orders[i][0]
        document.querySelector(`.prc--${i}`).value = `Rs.${orders[i][1]}`
        document.querySelector(`.quantity--${i}`).value = orders[i][2]
    }
}

// Calculating the total price.
const calcTotalPrice = function () {
    let sum = 0
    for (let i = 0; i < orders.length; i++) {
        sum += orders[i][1] * orders[i][2]
    }
    document.querySelector('.total-price').value = sum
}


// On click of confirm
document.querySelector('.confirm').addEventListener('click', function () {

    // Collecting the order data
    for (let i = 0; i < document.querySelectorAll('.order-row').length; i++) {
        const orderDetails = []
        for (let j = 0; j < 3; j++) {
            orderDetails.push(document.querySelectorAll('.order-row')[i].childNodes[j].textContent)
        }
        orders.push(orderDetails)
    }

    // Passing the data to the form.
    getData()
    // Passing the total price to the form.
    calcTotalPrice()
})





