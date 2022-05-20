use pyo3::prelude::*;
mod hello;


#[pymodule]
fn rust_toolkit(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<hello::Hello>()?;
    Ok(())
}
