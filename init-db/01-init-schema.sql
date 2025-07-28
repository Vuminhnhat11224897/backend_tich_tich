-- Database: Tích Tích App
-- Schema: Quản lý ví tiền cho trẻ em

-- Bảng 1: Thông tin khách hàng 
CREATE TABLE customers (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE customer_security (
    user_id INTEGER PRIMARY KEY,
    phone VARCHAR(10) UNIQUE NOT NULL,
    pin CHAR(6) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES customers(user_id) ON DELETE CASCADE
);

-- Bảng 2: Thông tin con cái 
CREATE TABLE children (
    child_id SERIAL PRIMARY KEY,
    parent_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES customers(user_id) ON DELETE CASCADE
);

-- Bảng 3: Wallet (Ví tiền) 
CREATE TABLE wallets (
    wallet_id SERIAL PRIMARY KEY,
    child_id INTEGER NOT NULL UNIQUE, -- Mỗi con chỉ có 1 wallet
    total INTEGER DEFAULT 0,
    savings INTEGER DEFAULT 0,
    charity INTEGER DEFAULT 0,
    buywhatyoulike INTEGER DEFAULT 0,
    study INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
);

-- Bảng 4: Transactions (Giao dịch) 
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    child_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL, -- split, spend
    wallet_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
);

-- Bảng 5 : Misssion
CREATE TABLE missions (
    mission_id SERIAL PRIMARY KEY,
    child_id INTEGER NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    wallet_type TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
);

-- Tạo indexes để tối ưu hiệu suất
CREATE INDEX idx_children_parent_id ON children(parent_id);
CREATE INDEX idx_wallets_child_id ON wallets(child_id);
CREATE INDEX idx_customers_phone ON customers(phone);

-- Trigger tự động tạo wallet khi thêm con cái
CREATE OR REPLACE FUNCTION create_wallet_for_child()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO wallets (child_id) VALUES (NEW.child_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_wallet
    AFTER INSERT ON children
    FOR EACH ROW
    EXECUTE FUNCTION create_wallet_for_child();

-- Schema đã sẵn sàng để sử dụng với SQLAlchemy
