# CODESTYLE

## Required content:

### 1. Class name

- **Class Based Views (CBV) / Function Based Views (FBV)**: Use `LoginView` with '**view**' at the end.

    _Examples_: `RegisterView`, `ManagementView`

<br>

- **Models Class**: Use `UserModel` with '**Model**' at the end.

    _Examples_: `CharacteristicsModel`, `CodeModel`

<br>

- **Form Class**: Use `UserForm` with '**Form**' at the end.

    _Examples_: `RegisterUserForm`, `UpdateInformationForm`

---

### 2. Identation rules

- Use **1 tab** per indentation level.  
- **Do not use spaces** for indentation.

---

### 3. Max length for lines of code

- Limit code files to a **maximum of 150 lines per view or class** to improve readability.

---

### 4. Comments and documentation format

- **Inline comments**: Use `//` for brief explanations.  
- **Block comments**: Use `/* */` to document functions or classes.

---

### 5. Commit names

- `feat/feature: add authentication user logic`
- `fix: change the logic for the sign-up`
- `docs/documentation: add CODESTYLE`

**Allow types**:

- `feat/feature`: New characteristics.
- `fix`: Fix errors.
- `docs/documentation`: change in documentation.

---

### 6. Branch names


- `feat/<feature-name> - feature/<feature-name>` → For new characteristics.
- `fix/<error-name>` → For change / fix errores.
- `docs/<update/add-documentation> - documentation/<update/add-documentation>` → For updates or changes in documentation.

**Examples**:

- `feat/addUserView`
- `fix/changeAuthenticationMethod`
- `docs/updateReadme`
- `feature/addUserView`
- `documentation/updateReadme`


### 7. PR information

Add the most important change to the name of the PR, also specific if the PR it's a `feat / fix / docs / feature / documentation`.

**Examples**:

- `feat: add authentication user logic`
- `fix: change the logic for the sign-up`
- `docs: add CODESTYLE`
- `feature: add authentication user logic`
- `documentation: add CODESTYLE`