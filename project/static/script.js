/* Name(s): Rosa Lisa Silipino, Jose Urrutia, Alberto Escalante
 * Class: CS 578 Final Project
 * File: script.js
 * Description: Basic interactive elements for webpage.
*/

// Fetch and display reminders
async function fetchReminders() {
    try {
        const response = await fetch("/reminders");
        const reminders = await response.json();
        const list = document.getElementById("reminderList");
        list.innerHTML = ""; // Clear existing reminders

        reminders.forEach(reminder => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <span>${reminder}</span>
                <button class="delete" onclick="deleteReminder('${reminder}')">Delete</button>
            `;
            list.appendChild(listItem);
        });
    } catch (error) {
        console.error("Error fetching reminders:", error);
    }
}

// Add a new reminder
async function addReminder() {
    const reminderInput = document.getElementById("reminderInput");
    const reminder = reminderInput.value.trim();

    if (!reminder) {
        alert("Please enter a valid reminder.");
        return;
    }

    try {
        await fetch("/reminders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ reminder }),
        });
        reminderInput.value = ""; // Clear input
        fetchReminders(); // Refresh list
    } catch (error) {
        console.error("Error adding reminder:", error);
    }
}

// Delete a reminder
async function deleteReminder(reminder) {
    try {
        await fetch("/reminders", {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ reminder }),
        });
        fetchReminders(); // Refresh list
    } catch (error) {
        console.error("Error deleting reminder:", error);
    }
}

// Load reminders on page load
window.onload = fetchReminders;
