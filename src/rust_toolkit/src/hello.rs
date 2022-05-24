use pyo3::prelude::*;


#[pyclass]
pub struct Hello {}

#[pymethods]
impl Hello {
    #[staticmethod]
    fn hello_world() -> PyResult<String> {
        Ok(String::from("Hello, world!"))
    }
}

