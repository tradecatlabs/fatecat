// Asio TCP Echo 服务器示例 - C++20 协程版本
// 演示如何使用 C++20 协程和 asio 库创建回环 echo 服务

import fmt;
import asio;
import std;

using asio::ip::tcp;
using asio::ip::udp;
using asio::awaitable;
using asio::co_spawn;
using asio::detached;
using asio::use_awaitable;
using namespace std::chrono_literals;

// ============= 协程版本的 Echo 会话 =============
awaitable<void> echo_session(tcp::socket socket) {
    try {
        char data[1024];
        for (;;) {
            std::size_t n = co_await socket.async_read_some(
                asio::buffer(data), 
                use_awaitable
            );
            
            std::println("  [服务器] 接收到 {} 字节: {}", 
                n, std::string_view(data, n));
            
            co_await asio::async_write(
                socket, 
                asio::buffer(data, n), 
                use_awaitable
            );
        }
    } catch (std::exception& e) {
        // 连接关闭或错误
        std::println("  [服务器] 会话结束: {}", e.what());
    }
}

// ============= 协程版本的 Echo 服务器 =============
awaitable<void> echo_server(unsigned short port) {
    auto executor = co_await asio::this_coro::executor;
    tcp::acceptor acceptor(executor, tcp::endpoint(tcp::v4(), port));
    
    std::println("  [服务器] 监听端口 {}", port);
    
    for (;;) {
        tcp::socket socket = co_await acceptor.async_accept(use_awaitable);
        std::println("  [服务器] 接受新连接");
        
        // 为每个连接启动一个协程
        co_spawn(executor, echo_session(std::move(socket)), detached);
    }
}

// ============= 协程版本的 Echo 客户端 =============
awaitable<void> echo_client(std::string host, std::string port, std::vector<std::string> messages) {
    auto executor = co_await asio::this_coro::executor;
    tcp::resolver resolver(executor);
    
    // 解析地址
    auto endpoints = co_await resolver.async_resolve(host, port, use_awaitable);
    
    // 连接到服务器
    tcp::socket socket(executor);
    co_await asio::async_connect(socket, endpoints, use_awaitable);
    std::println("  [客户端] 已连接到服务器");
    
    // 发送并接收消息
    for (const auto& msg : messages) {
        std::println("  [客户端] 发送: {}", msg);
        
        // 发送消息
        co_await asio::async_write(socket, asio::buffer(msg), use_awaitable);
        
        // 接收回显
        char reply[1024];
        std::size_t n = co_await socket.async_read_some(
            asio::buffer(reply, msg.size()), 
            use_awaitable
        );
        
        std::println("  [客户端] 接收回显: {}", std::string_view(reply, n));
    }
    
    std::println("  [客户端] 完成所有消息");
}

// ============= UDP 协程版本 =============
awaitable<void> udp_echo_server(unsigned short port) {
    auto executor = co_await asio::this_coro::executor;
    udp::socket socket(executor, udp::endpoint(udp::v4(), port));
    
    std::println("  [UDP服务器] 监听端口 {}", port);
    
    for (;;) {
        char data[1024];
        udp::endpoint sender_endpoint;
        
        std::size_t n = co_await socket.async_receive_from(
            asio::buffer(data),
            sender_endpoint,
            use_awaitable
        );
        
        std::println("  [UDP服务器] 接收: {}", std::string_view(data, n));
        
        co_await socket.async_send_to(
            asio::buffer(data, n),
            sender_endpoint,
            use_awaitable
        );
    }
}

awaitable<void> udp_echo_client(std::string host, std::string port, std::vector<std::string> messages) {
    auto executor = co_await asio::this_coro::executor;
    udp::resolver resolver(executor);
    
    auto endpoints = co_await resolver.async_resolve(
        udp::v4(), host, port, use_awaitable
    );
    
    udp::socket socket(executor, udp::endpoint(udp::v4(), 0));
    udp::endpoint receiver_endpoint = *endpoints.begin();
    
    for (const auto& msg : messages) {
        std::println("  [UDP客户端] 发送: {}", msg);
        
        co_await socket.async_send_to(
            asio::buffer(msg),
            receiver_endpoint,
            use_awaitable
        );
        
        char reply[1024];
        udp::endpoint sender_endpoint;
        std::size_t n = co_await socket.async_receive_from(
            asio::buffer(reply),
            sender_endpoint,
            use_awaitable
        );
        
        std::println("  [UDP客户端] 接收回显: {}", std::string_view(reply, n));
    }
    
    std::println("  [UDP客户端] 完成所有消息");
}

// ============= 示例函数 =============

void simple_tcp_echo_example() {
    std::println("\n");
    std::println("   示例 1: TCP Echo (C++20 协程版本)     ");
    std::println("\n");
    
    try {
        asio::io_context io_context;
        
        // 启动服务器协程
        std::println(" 启动 Echo 服务器，监听端口 8888...");
        co_spawn(io_context, echo_server(8888), detached);
        
        // 在单独的线程中运行 io_context
        std::thread server_thread([&io_context]() {
            io_context.run();
        });
        
        // 等待服务器启动
        std::this_thread::sleep_for(100ms);
        
        // 启动客户端协程
        std::println("\n 启动客户端...");
        asio::io_context client_io;
        
        co_spawn(client_io, 
            echo_client("127.0.0.1", "8888", {
                "Hello, Asio!",
                "测试中文消息",
                "C++20 Coroutines"
            }), 
            detached
        );
        
        // 运行客户端
        client_io.run();
        
        std::println("\n TCP Echo 测试完成！");
        
        // 停止服务器
        io_context.stop();
        server_thread.join();
        
    } catch (const std::exception& e) {
        std::println(" 错误: {}", e.what());
    }
}

void multiple_clients_example() {
    std::println("\n");
    std::println("   示例 2: 多客户端并发 (协程版本)       ");
    std::println("\n");
    
    try {
        asio::io_context io_context;
        
        // 启动服务器
        std::println(" 启动 Echo 服务器，监听端口 8889...");
        co_spawn(io_context, echo_server(8889), detached);
        
        std::thread server_thread([&io_context]() {
            io_context.run();
        });
        
        std::this_thread::sleep_for(100ms);
        
        // 启动多个客户端协程
        asio::io_context client_io;
        
        for (int i = 1; i <= 3; ++i) {
            std::vector<std::string> messages;
            for (int j = 1; j <= 2; ++j) {
                messages.push_back("客户端 " + std::to_string(i) + " 的消息 " + std::to_string(j));
            }
            
            co_spawn(client_io,
                echo_client("127.0.0.1", "8889", std::move(messages)),
                detached
            );
        }
        
        // 运行所有客户端协程
        client_io.run();
        
        std::println("\n 多客户端测试完成！");
        
        io_context.stop();
        server_thread.join();
        
    } catch (const std::exception& e) {
        std::println(" 错误: {}", e.what());
    }
}

void udp_echo_example() {
    std::println("\n");
    std::println("   示例 3: UDP Echo (C++20 协程版本)     ");
    std::println("\n");
    
    try {
        asio::io_context io_context;
        
        // 启动 UDP 服务器
        std::println(" 启动 UDP Echo 服务器，监听端口 8890...");
        co_spawn(io_context, udp_echo_server(8890), detached);
        
        std::thread server_thread([&io_context]() {
            io_context.run();
        });
        
        std::this_thread::sleep_for(100ms);
        
        // 启动 UDP 客户端
        std::println("\n 发送 UDP 消息...");
        asio::io_context client_io;
        
        co_spawn(client_io,
            udp_echo_client("127.0.0.1", "8890", {
                "UDP消息1",
                "UDP消息2", 
                "UDP消息3"
            }),
            detached
        );
        
        client_io.run();
        
        std::println("\n UDP Echo 测试完成！");
        
        io_context.stop();
        server_thread.join();
        
    } catch (const std::exception& e) {
        std::println(" 错误: {}", e.what());
    }
}

// ============= 协程超时示例 =============
awaitable<void> timeout_example_client() {
    auto executor = co_await asio::this_coro::executor;
    
    // 创建一个定时器
    asio::steady_timer timer(executor);
    timer.expires_after(2s);
    
    std::println("  [超时示例] 等待 2 秒...");
    co_await timer.async_wait(use_awaitable);
    std::println("  [超时示例] 2 秒已过！");
}

void timeout_example() {
    std::println("\n");
    std::println("   示例 4: 协程超时控制                  ");
    std::println("\n");
    
    try {
        asio::io_context io_context;
        
        co_spawn(io_context, timeout_example_client(), detached);
        
        io_context.run();
        
        std::println("\n 超时示例完成！");
        
    } catch (const std::exception& e) {
        std::println(" 错误: {}", e.what());
    }
}

// ============= 并发协程示例 =============
awaitable<void> concurrent_task(int id, int delay_ms) {
    auto executor = co_await asio::this_coro::executor;
    asio::steady_timer timer(executor);
    
    std::println("  [任务 {}] 开始，将延迟 {} 毫秒", id, delay_ms);
    
    timer.expires_after(std::chrono::milliseconds(delay_ms));
    co_await timer.async_wait(use_awaitable);
    
    std::println("  [任务 {}] 完成！", id);
}

void concurrent_coroutines_example() {
    std::println("\n");
    std::println("   示例 5: 并发协程任务                  ");
    std::println("\n");
    
    try {
        asio::io_context io_context;
        
        std::println(" 启动 5 个并发协程任务...\n");
        
        // 启动多个协程，它们会并发执行
        co_spawn(io_context, concurrent_task(1, 500), detached);
        co_spawn(io_context, concurrent_task(2, 300), detached);
        co_spawn(io_context, concurrent_task(3, 700), detached);
        co_spawn(io_context, concurrent_task(4, 200), detached);
        co_spawn(io_context, concurrent_task(5, 400), detached);
        
        io_context.run();
        
        std::println("\n 所有协程任务完成！");
        
    } catch (const std::exception& e) {
        std::println(" 错误: {}", e.what());
    }
}

// ============= 主函数 =============

int main() {
    std::println("");
    std::println("   Asio Echo 服务 - C++20 协程版本               ");
    std::println("   Modern Async I/O with Coroutines              ");
    std::println("");
    
    try {
        // 运行所有示例
        simple_tcp_echo_example();
        std::this_thread::sleep_for(200ms);
        
        multiple_clients_example();
        std::this_thread::sleep_for(200ms);
        
        udp_echo_example();
        std::this_thread::sleep_for(200ms);
        
        timeout_example();
        std::this_thread::sleep_for(200ms);
        
        concurrent_coroutines_example();
        
        std::println("\n==================================================");
        std::println(" 所有示例完成！C++20 协程让异步代码更简洁！");
        std::println("==================================================\n");
        
    } catch (const std::exception& e) {
        std::println("\n 程序错误: {}", e.what());
        return 1;
    }
    
    return 0;
}
