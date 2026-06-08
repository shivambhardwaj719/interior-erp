# Interior ERP

Interior ERP is a customized Frappe/ERPNext application specifically designed for **Interior Design and Architecture Firms**. It streamlines project pipelines, manages client CRM, tracks expenses and budgets, handles site visits, and provides rich analytics through a beautiful modular interface.

## 🚀 Key Features

*   **Modular Workspace Hierarchy**: Clean, nested sidebar navigation (CRM, Projects, Finance, Procurement, Reports, Employees, Settings).
*   **Custom DocTypes**: Specialized data structures for `Site Visit` scheduling and `Proposal BOQ` (Bill of Quantities) tracking.
*   **Dynamic Analytics Dashboards**: Every core module automatically generates real-time metric cards (e.g., *Total Customers*, *Total Expenses*) and Monthly Line Charts to visualize data trends.
*   **Vite React Analytics**: A dedicated React-based interactive Pipeline Dashboard natively embedded into the Frappe interface for high-level business intelligence.
*   **Automated Seeding Engine**: A built-in Python data generation script capable of automatically spinning up dummy Leads, Customers, Projects, Budgets, and Journal Entries to test the system out of the box.

---

## 🛠️ Installation

1. Navigate to your frappe-bench directory.
2. Get the app and install it on your site:
```bash
bench get-app interior_erp https://github.com/your-repo/interior_erp.git
bench --site [your-site-name] install-app interior_erp
```
*(If you are running via Docker, make sure to mount or copy the app into your `frappe-bench/apps/` directory.)*

---

## 🏗️ System Initialization

To instantly format your workspace to the Interior ERP standard and generate testing data, use the provided backend scripts.

### 1. Generate Test Data
Run the seeding script to automatically populate your site with 50+ records across Leads, Customers, Projects, Budgets, Expenses, Suppliers, and Items.
```bash
bench execute interior_erp.seed_data.generate_dummy_data
```

### 2. Configure Workspaces & Dashboards
Run the workspace setup script. This hides all default ERPNext workspaces, builds the clean Interior ERP hierarchical menu, and dynamically injects Analytics widgets (Number Cards & Charts) into every module.
```bash
bench set-config developer_mode 0
bench execute interior_erp.setup_workspace.create_and_hide_workspaces
bench clear-cache
```

---

## 📊 Modules Breakdown

*   **Dashboard**: High-level system overview including the custom Vite React analytics.
*   **CRM**: Leads, Customers, and Follow-ups.
*   **Projects**: Project execution, Site Visits, Proposal BOQs, and Design Workflows.
*   **Finance**: Journal Entries (Expenses), Payment Entries, and Project Budgets.
*   **Procurement**: Material Requests, Purchase Orders, Suppliers, and Items.
*   **Reports**: Quick shortcuts to General Ledger, Accounts Receivable, Purchase Register, etc.
*   **Employees**: HR Management.
*   **Settings**: Permissions, Data Imports, User configurations.

---

## 📜 License
MIT
