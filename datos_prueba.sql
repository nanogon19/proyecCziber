-- Script SQL para poblar datos de prueba

-- Insertar empresas
INSERT INTO companies (id_emp, name) VALUES 
('empresa-1', 'Gamma Consultores'),
('empresa-2', 'Tech Solutions'),
('empresa-3', 'Data Analytics Inc');

-- Insertar aplicaciones
INSERT INTO applications (id_app, nombre) VALUES 
('app-1', 'DataSage'),
('app-2', 'Business Intelligence'),
('app-3', 'Customer Analytics');

-- Insertar modelos
INSERT INTO models (id_model, nombre, version, app_id) VALUES 
('model-1', 'GPT-4', '1.0', 'app-1'),
('model-2', 'Claude', '2.1', 'app-1'),
('model-3', 'Llama', '3.0', 'app-1');
