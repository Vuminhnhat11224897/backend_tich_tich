-- Database: Tích Tích App
-- Schema: Quản lý ví tiền cho trẻ em

-- Bảng 1: Thông tin khách hàng (chỉ có UserID và phone)
CREATE TABLE customers (
    user_id SERIAL PRIMARY KEY,
    phone VARCHAR(15) UNIQUE NOT NULL,  -- Số điện thoại làm mật khẩu
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Bảng 2: Thông tin con cái (bỏ gender, date_of_birth)
CREATE TABLE children (
    child_id SERIAL PRIMARY KEY,
    parent_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (parent_id) REFERENCES customers(user_id) ON DELETE CASCADE
);

-- Bảng 3: Wallet (Ví tiền) - giữ nguyên
CREATE TABLE wallets (
    wallet_id SERIAL PRIMARY KEY,
    child_id INTEGER NOT NULL UNIQUE, -- Mỗi con chỉ có 1 wallet
    total DECIMAL(12,2) DEFAULT 0.00,
    savings DECIMAL(12,2) DEFAULT 0.00,
    charity DECIMAL(12,2) DEFAULT 0.00,
    spending DECIMAL(12,2) DEFAULT 0.00,
    bought DECIMAL(12,2) DEFAULT 0.00,
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

-- Trigger cập nhật total khi thay đổi ví
CREATE OR REPLACE FUNCTION update_total_wallet()
RETURNS TRIGGER AS $$
BEGIN
    NEW.total = NEW.savings + NEW.charity + NEW.spending + NEW.bought;
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_total
    BEFORE UPDATE ON wallets
    FOR EACH ROW
    EXECUTE FUNCTION update_total_wallet();

-- Schema đã sẵn sàng để sử dụng với SQLAlchemy
-- Dữ liệu sẽ được thêm thông qua Python/SQLAlchemy
