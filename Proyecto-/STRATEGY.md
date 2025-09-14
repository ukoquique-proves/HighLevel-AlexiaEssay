# Project Strategy: CRM Automation

## 1. Current Goal and Status

Our primary objective is to build a robust, end-to-end CRM automation workflow. We have successfully completed the initial phases, including lead validation and mock AI ad generation.

---

### Historical Context

For details on previous pivots, including the Ariaia integration and product commercialization strategy, see [BUSINESS_STRATEGY_UPDATE.md](./BUSINESS_STRATEGY_UPDATE.md).

We are currently in **Phase 3: CRM Integration**. However, direct integration with the HighLevel API is **currently blocked**. This is because the available HighLevel account is a free/trial version, which does not grant the necessary API access to create private applications and generate authentication tokens.

---

## 2. The Strategic Pivot: Mock Integration

To ensure the project continues to advance despite the external limitation, we have implemented a strategic pivot:

**We are proceeding with a Mock HighLevel Integration.**

This involves using a new workflow, `crm-lead-workflow-phase3-mock.json`, which perfectly simulates the responses of the real HighLevel API. This strategy allows us to:

-   **Test the Full Workflow**: We can validate the entire end-to-end logic, from webhook trigger to final response, without needing real credentials.
-   **Maintain Project Momentum**: Development is not halted while waiting for an account upgrade.
-   **Be Ready for Production**: The workflow is designed to be a "plug-and-play" system. Once API access is available, the mock node can be easily swapped with the real HighLevel nodes.

---

## 3. How This Strategy Connects Our Documentation

This section explains how to navigate the project's documentation in the context of our current strategy.

---

## 4. Business Vertical Extensibility

The workflow is designed to support multiple business types, starting with Fashion SME (Small and Medium Enterprise) and generic businesses. The `businessType` field determines which set of fields and validation rules apply.

- If `businessType` is `"fashion_sme"`, the workflow expects and validates Fashion SME-specific fields (e.g., `fashionSector`, `currentChannels`, `brandDifferentiation`, etc.).
- If another type or omitted, only the generic fields are required, and the workflow remains compatible with other business verticals.

This approach allows the system to be easily extended in the future for new industries or business types, simply by adding new validation and processing logic for each type.

### Example Input Schema

```json
{
  "businessType": "fashion_sme",  // or "generic", "other"
  "name": "Maria Rodriguez",
  "email": "maria@fashionstore.com",
  "phone": "+57 300 123 4567",
  "service": "marketing",
  "company": "Boutique Maria",
  "budget": "500-1000",
  "message": "Necesito ayuda con marketing digital para mi tienda de ropa femenina",
  // Fashion SME-specific fields (only required if businessType is "fashion_sme"):
  "fashionSector": "moda-femenina",           // moda-femenina, moda-masculina, infantil, accesorios, etc.
  "country": "colombia",
  "city": "Bogotá",
  "currentChannels": ["instagram", "facebook", "tienda-fisica"],
  "monthlySales": "1000-5000",
  "marketingBudget": "500-1000",
  "hasProductImages": true,
  "brandDifferentiation": "Ropa hecha a mano con materiales ecológicos",
  "objective": "aumentar-ventas"             // aumentar-ventas, captar-leads, lanzar-producto, fidelizar-clientes
}
```

-   **`FIRST_STEPS.md`**
    -   **Purpose**: The starting point for any new team member.
-   **`ROL-DE-HECTOR`**
    -   **Purpose**: Defines the responsibilities and phases for Hector, focused on API connections, N8N orchestration, and automation. See also `HECTOR-STEPS.md` for Hector's operational step-by-step guide.
    -   **Testing Tool**: Use `hector-test-dashboard.html` for comprehensive web-based testing of all workflow inputs/outputs without console dependency.
    -   **Relation**: It introduces the project's high-level **architectural vision** (the hybrid n8n + Python model). You should read this file first to understand our goals.

-   **`STRATEGY.md` (This Document)**
    -   **Purpose**: Explains the *current, practical plan* of action.
    -   **Relation**: This document details the **mock integration workaround** and clarifies which parts of the project are active and which are on hold. It connects the vision from `FIRST_STEPS.md` to our day-to-day work.

-   **`PYTHON_INCLUSION.md`**
    -   **Purpose**: Details the rationale and long-term roadmap for our hybrid n8n + Python architecture.
    -   **Relation**: This document describes the **future-state** we are building towards. Our first planned Python component, the `highlevel_token_manager.py` script, is currently on hold because it depends on the real HighLevel API.

-   **`HIGHLEVEL_SETUP_GUIDE.md`** & **`HIGHLEVEL_AUTH_TOKEN_GUIDE.md`**
    -   **Purpose**: These guides contain the technical instructions for connecting to the **real** HighLevel API.
    -   **Relation**: Due to the account limitations, these documents are currently **ON HOLD**. They are preserved for the future, when a full HighLevel subscription is available.

---

## 4. The Path Forward

Our immediate plan is clear and actionable:

1.  **Test the Mock Workflow**: The immediate next step is to import and test the `crm-lead-workflow-phase3-mock.json` file to confirm our entire business logic is sound.
2.  **Proceed with Python Development (Optional)**: We can begin developing other Python microservices for tasks that don't depend on the HighLevel API, such as more advanced AI text generation or lead scoring logic.
3.  **Await HighLevel Access**: Once a full HighLevel account is available, we will execute the plan detailed in the `HIGHLEVEL_AUTH_TOKEN_GUIDE.md` and `HIGHLEVEL_SETUP_GUIDE.md` to switch from the mock to the real integration.
