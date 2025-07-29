-- 1. Customer
CREATE TABLE customers (
    parent_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- 2. Security
CREATE TABLE security (
    parent_id SERIAL PRIMARY KEY,
    phone VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES customers(parent_id) ON DELETE CASCADE
);

-- 3. Child
CREATE TABLE children (
    child_id SERIAL PRIMARY KEY,
    parent_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 0),
    coin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES customers(parent_id) ON DELETE CASCADE
);

-- 4. Character Own
CREATE TABLE character_own (
    character_id SERIAL PRIMARY KEY,
    child_id INTEGER UNIQUE NOT NULL,
    level INTEGER DEFAULT 1,
    coin_to_upgrade INTEGER DEFAULT 0,
    image_corresponding_level TEXT,
    effect_corresponding_level TEXT,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
);

-- 5. Wallet
CREATE TABLE wallets (
    wallet_id SERIAL PRIMARY KEY,
    child_id INTEGER UNIQUE NOT NULL,
    total INTEGER DEFAULT 0,
    charity INTEGER DEFAULT 0,
    savings INTEGER DEFAULT 0,
    study INTEGER DEFAULT 0,
    joy INTEGER DEFAULT 0,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
);

-- 6. Transaction
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    wallet_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL, -- split, spending
    wallet_type TEXT, -- charity, study, saving, buywhatyoulike
    purpose VARCHAR(255),
    time_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wallet_id) REFERENCES wallets(wallet_id) ON DELETE CASCADE
);

-- 7. Mission
CREATE TABLE missions (
    mission_id SERIAL PRIMARY KEY,
    purpose VARCHAR(255) NOT NULL,
    wallet_type TEXT,
    amount INTEGER,
    child_id INTEGER NOT NULL,
    mission_progress_id INTEGER,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
    -- mission_progress_id sẽ được liên kết ở bảng mission_progress
);

-- 8. Mission Progress
CREATE TABLE mission_progress (
    mission_progress_id SERIAL PRIMARY KEY,
    mission_id INTEGER NOT NULL UNIQUE,
    time_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_end TIMESTAMP,
    status VARCHAR(50),
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
);

-- 9. Subscription
CREATE TABLE subscriptions (
    parent_id SERIAL PRIMARY KEY,
    time_start TIMESTAMP,
    time_end TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    type VARCHAR(50),
    time_to_use INTEGER,
    FOREIGN KEY (parent_id) REFERENCES customers(parent_id) ON DELETE CASCADE
);

-- 10. ActionLogs
CREATE TABLE action_logs (
    action_id SERIAL PRIMARY KEY,
    time_begin TIMESTAMP,
    time_end TIMESTAMP,
    action_type VARCHAR(50),
    action_detail TEXT,
    child_id INTEGER,
    transaction_id INTEGER,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE SET NULL
);

-- 11. Game (bảng phần thưởng)
CREATE TABLE game_rewards (
    reward_id SERIAL PRIMARY KEY,
    reward_type VARCHAR(50), -- nhap, chi, mission_reward
    value INTEGER NOT NULL,
    description TEXT
);

CREATE INDEX idx_children_parent_id ON children(parent_id);
CREATE INDEX idx_character_own_child_id ON character_own(child_id);
CREATE INDEX idx_wallets_child_id ON wallets(child_id);
CREATE INDEX idx_transactions_wallet_id ON transactions(wallet_id);
CREATE INDEX idx_missions_child_id ON missions(child_id);
CREATE INDEX idx_mission_progress_mission_id ON mission_progress(mission_id);
CREATE INDEX idx_action_logs_child_id ON action_logs(child_id);
CREATE INDEX idx_action_logs_transaction_id ON action_logs(transaction_id);

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
