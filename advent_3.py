def _parse_memory() -> list[str]:
    with open('input/input_3_1.txt') as file:
        return [line for line in file]


def _scan_and_calculate_mul_ops(
    line: str,
    activator: str | None = None,
    deactivator: str | None = None,
) -> int:
    calculated = 0
    cursor = 0
    operator = "mul("
    ops_len = len(operator)
    active = True
    
    while cursor < len(line) - ops_len - 1:
        if (
            active
            or (
                being_activated := (
                    not active
                    and activator
                    and line[cursor:(cursor + len(activator))] == activator
                )
            )
        ):
            if not active and being_activated:
                active = True
                cursor += 1
                continue
                
            if deactivator and line[cursor:(cursor + len(deactivator))] == deactivator:
                active = False
                cursor += 1
                continue
            
            if line[cursor:(cursor + ops_len)] != operator:
                cursor += 1
                continue
            
            where = line.find(")", cursor)
            if where < 0:
                return calculated
            
            arguments = line[(cursor + ops_len):where].split(",")
            if len(arguments) > 2:
                cursor += 1
                continue
            try:
                calculated += (int(arguments[0]) * int(arguments[1]))
            except ValueError:
                pass
            except IndexError:
                pass
            finally:
                cursor += 1
        else:
            cursor += 1
    
    return calculated


if __name__ == '__main__':
    lines = _parse_memory()
    print(_scan_and_calculate_mul_ops(str.join("", lines)))
    print(_scan_and_calculate_mul_ops(str.join("", lines), "do()", "don't()"))
