document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1;

    const elements = {
        loadBtn: document.getElementById('loadUsersBtn'),
        prevBtn: document.getElementById('prevPage'),
        nextBtn: document.getElementById('nextPage'),
        pageInfo: document.getElementById('pageInfo'),
        userCount: document.getElementById('userCount'),
        tableBody: document.getElementById('usersTableBody')
    };

    const loadUsers = async (count = 20) => {
        try {
            const response = await fetch(`/api/load-users?count=${count}`);
            const data = await response.json();
            if (data.status === 'success') {
                await fetchUsers(currentPage);
            }
        } catch (error) {
            console.error("Load error:", error);
        }
    };

    const fetchUsers = async (page = 1) => {
        const itemsPerPage = parseInt(elements.userCount.value, 10) || 10;
        try {
            const response = await fetch(`/api/users?page=${page}&limit=${itemsPerPage}`);
            const data = await response.json();
            if (data.users) {
                renderUsers(data.users);
                updatePagination();
            }
        } catch (error) {
            console.error("Fetch error:", error);
        }
    };

    const renderUsers = (users) => {
        elements.tableBody.innerHTML = users.map(user => `
            <tr>
                <td><img src="${user.photo}" class="user-photo"></td>
                <td>${user.first_name} ${user.last_name}</td>
                <td>${user.gender}</td>
                <td>${user.email}</td>
                <td>${user.phone}</td>
                <td>${user.place}</td>
                <td><a href="/${user.id}" class="btn btn-sm btn-outline-primary">View</a></td>
            </tr>
        `).join('');
    };

    const updatePagination = () => {
        elements.prevBtn.disabled = currentPage <= 1;
        elements.pageInfo.textContent = `Page ${currentPage}`;
    };

    elements.loadBtn.addEventListener('click', () => {
        const count = parseInt(elements.userCount.value, 10) || 20;
        currentPage = 1;  // сбрасываем на первую страницу
        loadUsers(count);
    });

    elements.prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            fetchUsers(currentPage);
        }
    });

    elements.nextBtn.addEventListener('click', () => {
        currentPage++;
        fetchUsers(currentPage);
    });

    fetchUsers(currentPage);
});
