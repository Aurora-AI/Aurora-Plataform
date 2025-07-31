# NestJS

## O que é
Framework Node.js para construção de APIs escaláveis e eficientes.

## Como usamos no projeto
Utilizado para criar os serviços do backend, com arquitetura modular.

## Exemplos práticos
```typescript
@Controller('users')
export class UserController {
  @Get()
  findAll() {
    return this.userService.findAll();
  }
}
```

## Links úteis
- [NestJS Documentation](https://docs.nestjs.com/)
- [Tutorial rápido](https://docs.nestjs.com/first-steps)

## Erros comuns e soluções
Erro de injeção de dependência: ver error-20250721-1235-exemplo.md
