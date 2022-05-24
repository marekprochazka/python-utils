use pyo3::prelude::*;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct SubdirConf {
    dirname: String,
    extensions: Vec<String>,
}

impl SubdirConf {
    fn new(dirname: String, extensions: Vec<String>) -> SubdirConf {
        SubdirConf {
            dirname,
            extensions,
        }
    }
}

#[pyclass]
pub struct FolderAdministrator {
    config: Vec<SubdirConf>,
    verbose: bool,
}

#[pymethods]
impl FolderAdministrator {
    #[new]
    fn load(verbose: bool) -> PyResult<Self> {
        let mut fadm = FolderAdministrator { config: Vec::new(),verbose: verbose};
        fadm.load_config()?;
        Ok(fadm)
    }

    fn load_config(&mut self) -> std::io::Result<()> {
        if self.verbose {
            println!("Loading config...");
        }
        let config_str = fs::read_to_string("FolderAdministratorConfig.json")?;
        let config: serde_json::Value = serde_json::from_str(&config_str)?;
        if config.as_array().is_some() {
            for subdir in config.as_array().unwrap() {
                let dirname = subdir["dirname"].as_str().unwrap();
                let extensions = subdir["extensions"].as_array().unwrap();
                let mut extensions_vec: Vec<String> = Vec::new();
                for extension in extensions {
                    extensions_vec.push(extension.as_str().unwrap().to_string());
                }
                self.config
                    .push(SubdirConf::new(dirname.to_string(), extensions_vec));
            }
        }
        Ok(())
    }

    fn create_dirs(&self) {
        if self.verbose {
            println!("Looking for existing directories...");
        }
        for subdir in &self.config {
            let dirname = subdir.dirname.clone();
            let path = Path::new(".").join(dirname.clone());
            if !path.exists() {
                fs::create_dir(path).unwrap();
                if self.verbose {
                    println!("Created directory {}", dirname);
                }
            }
        }
    }

    fn move_files_to_dirs(&self) {
        self.create_dirs();
        let files = fs::read_dir("./").unwrap();
        for file in files {
            let file = file.unwrap();
            let path = file.path();
            if path.is_file() {
                let extension = path
                    .clone()
                    .extension()
                    .unwrap()
                    .to_os_string()
                    .into_string()
                    .unwrap();
                for subdir in &self.config {
                    if subdir.extensions.contains(&extension) {
                        let dirname = subdir.dirname.clone();
                        let filename = path
                            .clone()
                            .file_name()
                            .unwrap()
                            .to_os_string()
                            .into_string()
                            .unwrap();
                        let new_path = Path::new(".").join(dirname).join(filename);
                        fs::rename(path.clone(), new_path.clone()).unwrap();
                        if self.verbose {
                            println!(
                                "Moved {} to {}",
                                path.to_str().unwrap(),
                                new_path.to_str().unwrap()
                            );
                        }
                    }
                }
            }
        }
    }

    fn print_config(&self) {
        println!("{:?}", self.config);
    }
}
