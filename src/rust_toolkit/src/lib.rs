use pyo3::prelude::*;
mod hello;
mod folder_admin;


#[pymodule]
fn rust_toolkit(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<hello::Hello>()?;
    m.add_class::<folder_admin::FolderAdministrator>()?;
    Ok(())
}
