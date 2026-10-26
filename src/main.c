#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *buffer; // Pointer to the buffer(In Heap)
    size_t buffer_length; // Length of the buffer (how many bytes it holds), like size of the cell in Heap
    ssize_t data_length; // Length of the data in the buffer (input length in bytes)
} InputBuffer;

//constructor for InputBuffer
InputBuffer *new_input_buffer(void) {
    InputBuffer *input_buffer = malloc(sizeof(InputBuffer));
    input_buffer->buffer = NULL;
    input_buffer->buffer_length = 0;
    input_buffer->data_length = 0;

    return input_buffer;
}

void print_prompt(void){printf("db > ");}

void read_input(InputBuffer *input_buffer){
    ssize_t bytes_read = getline(&(input_buffer->buffer), &(input_buffer->buffer_length), stdin);
    if(bytes_read <= 0){
        printf("Error reading input\n");
        exit(EXIT_FAILURE);
    }
    
    input_buffer -> data_length = bytes_read - 1; // Ignore trailing newline
    input_buffer -> buffer[bytes_read - 1] = 0; // Null terminate string
}

void close_input_buffer(InputBuffer *input_buffer){
    free(input_buffer->buffer);
    free(input_buffer);
}

// Meta-commands (".exit") are for the REPL itself, not SQL.
typedef enum {
    META_COMMAND_SUCCESS,
    META_COMMAND_UNRECOGNIZED_COMMAND
} MetaCommandResult;

typedef enum {
    PREPARE_SUCCESS,
    PREPARE_UNRECOGNIZED_STATEMENT
} PrepareResult;

typedef enum {
    STATEMENT_INSERT,
    STATEMENT_SELECT
} StatementType;

// The "compiled" statement: the tokenizer's output, the executor's input.
typedef struct {
    StatementType type;
} Statement;

MetaCommandResult do_meta_command(InputBuffer *input_buffer){
    if (strcmp(input_buffer->buffer, ".exit") == 0){
        close_input_buffer(input_buffer);
        exit(EXIT_SUCCESS);
    }
    return META_COMMAND_UNRECOGNIZED_COMMAND;
}

// Front-end: text -> Statement. Only decides *which* statement it is.
PrepareResult prepare_statement(InputBuffer *input_buffer, Statement *statement){
    // "insert" carries arguments after it, so compare only the first 6 bytes.
    if (strncmp(input_buffer->buffer, "insert", 6) == 0){
        statement->type = STATEMENT_INSERT;
        return PREPARE_SUCCESS;
    }
    // "select" has no arguments yet, so the whole line must match.
    if (strcmp(input_buffer->buffer, "select") == 0){
        statement->type = STATEMENT_SELECT;
        return PREPARE_SUCCESS;
    }
    return PREPARE_UNRECOGNIZED_STATEMENT;
}

// Back-end ("virtual machine"): runs a Statement. Knows nothing about text.
void execute_statement(Statement *statement){
    switch (statement->type){
        case STATEMENT_INSERT:
            // TODO: write the row into the table (next stage)
            break;
        case STATEMENT_SELECT:
            // TODO: read rows from the table (next stage)
            break;
    }
}

int main(void){
    InputBuffer *input_buffer = new_input_buffer();
    while(true){
        print_prompt();
        read_input(input_buffer);

        if (input_buffer->buffer[0] == '.'){
            switch (do_meta_command(input_buffer)){
                case META_COMMAND_SUCCESS:
                    continue;
                case META_COMMAND_UNRECOGNIZED_COMMAND:
                    printf("Unrecognized command '%s'.\n", input_buffer->buffer);
                    continue;
            }
        }

        Statement statement;
        switch (prepare_statement(input_buffer, &statement)){
            case PREPARE_SUCCESS:
                break;
            case PREPARE_UNRECOGNIZED_STATEMENT:
                printf("Unrecognized keyword at start of '%s'.\n", input_buffer->buffer);
                continue;
        }

        execute_statement(&statement);
        printf("Executed.\n");
    }
}
