IF OBJECT_ID('dbo.audit_log', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.audit_log (
        id BIGINT IDENTITY(1,1) PRIMARY KEY,
        event_ts DATETIME2 NOT NULL,
        actor NVARCHAR(200) NOT NULL,
        action NVARCHAR(200) NOT NULL,
        entity_type NVARCHAR(100) NOT NULL,
        entity_id NVARCHAR(100) NOT NULL,
        status NVARCHAR(50) NOT NULL,
        reason_code NVARCHAR(100) NOT NULL,
        request_json NVARCHAR(MAX) NULL,
        response_json NVARCHAR(MAX) NULL
    );
END;

IF OBJECT_ID('dbo.business_rules', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.business_rules (
        rule_key NVARCHAR(100) PRIMARY KEY,
        rule_value NVARCHAR(MAX) NOT NULL
    );
END;

IF OBJECT_ID('dbo.fact_sales', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.fact_sales (
        id BIGINT IDENTITY(1,1) PRIMARY KEY,
        product_id NVARCHAR(100) NOT NULL,
        sale_date DATE NOT NULL,
        unit_price DECIMAL(18,2) NOT NULL,
        quantity INT NOT NULL,
        revenue DECIMAL(18,2) NOT NULL,
        cost DECIMAL(18,2) NOT NULL,
        channel NVARCHAR(100) NULL,
        region NVARCHAR(100) NULL
    );
END;
